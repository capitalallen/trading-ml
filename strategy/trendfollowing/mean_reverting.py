import mlfinlab as ml
import numpy as np
import pandas as pd
import pyfolio as pf
import timeit

from sklearn.utils import resample
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.metrics import roc_curve
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import datasets
from joblib import dump, load

import matplotlib.pyplot as plt


class Mean_reverting:
    def __init__(self, datafile):
        self.data = self.read_data(datafile)
        self.datafile = datafile
    # read data, split data

    def read_data(self, fileName):
        # 1 Read in data
        if not fileName:
            print("invalid file - read_data")
            return
        data = pd.read_csv(fileName, encoding='utf-8')
        i = int(data.shape[0]*0.8)
        if "timestamp" in list(data.columns.values):
            data = data.rename(columns={"timestamp": "date_time"})
        self.start_date = str(data.date_time[0]).split()[0]
        self.end_date = str(data.date_time[i]).split()[0]
        self.test_date = str(data.date_time[i+1]).split()[0]
        data.index = pd.to_datetime(data['date_time'])
        data = data.drop('date_time', axis=1)
        return data

    def relative_strength_index(self, df, n):
        """Calculate Relative Strength Index(RSI) for given data.
        https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py

        :param df: pandas.DataFrame
        :param n: 
        :return: pandas.DataFrame
        """
        i = 0
        UpI = [0]
        DoI = [0]
        while i + 1 <= df.index[-1]:
            UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
            DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
            if UpMove > DoMove and UpMove > 0:
                UpD = UpMove
            else:
                UpD = 0
            UpI.append(UpD)
            if DoMove > UpMove and DoMove > 0:
                DoD = DoMove
            else:
                DoD = 0
            DoI.append(DoD)
            i = i + 1
        UpI = pd.Series(UpI)
        DoI = pd.Series(DoI)
        PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
        NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
        RSI = pd.Series(round(PosDI * 100. / (PosDI + NegDI)),
                        name='RSI_' + str(n))
        # df = df.join(RSI)
        return RSI

    def get_rsi(self, data, window=14):
        df = data.copy(deep=True).reset_index()
        rsi = self.relative_strength_index(df, window)
        rsi_df = pd.Series(data=rsi.values, index=data.index)
        return rsi_df

    def bbands(self, close_prices, window, no_of_stdev):
        # rolling_mean = close_prices.rolling(window=window).mean()
        # rolling_std = close_prices.rolling(window=window).std()
        rolling_mean = close_prices.ewm(span=window).mean()
        rolling_std = close_prices.ewm(span=window).std()

        upper_band = rolling_mean + (rolling_std * no_of_stdev)
        lower_band = rolling_mean - (rolling_std * no_of_stdev)

        return rolling_mean, upper_band, lower_band
    # 3

    def add_bbands(self, window=50, no_of_stdev=1.5):
        # compute bands
        self.data['avg'], self.data['upper'], self.data['lower'] = self.bbands(
            self.data['close'], window, no_of_stdev=no_of_stdev)
    # 4 5

    def add_rsi(self, window=14):
        # Compute RSI
        rsi_df = self.get_rsi(self.data, window=window)
        self.data['rsi'] = pd.Series(data=rsi_df.values, index=self.data.index)

        # Drop the NaN values from our data set
        self.data.dropna(axis=0, how='any', inplace=True)

    # 6
    def compute_side(self):
        # Compute sides
        self.data['side'] = np.nan

        long_signals = (self.data['close'] <= self.data['lower'])
        short_signals = (self.data['close'] >= self.data['upper'])

        self.data.loc[long_signals, 'side'] = 1
        self.data.loc[short_signals, 'side'] = -1

        # Remove Look ahead biase by lagging the signal
        self.data['side'] = self.data['side'].shift(1)

        # Save the raw data
        self.raw_data = self.data.copy()
        # Drop the NaN values from our data set
        self.data.dropna(axis=0, how='any', inplace=True)

    # 8
    def cusum_filter(self, lookback=50):
        # Compute daily volatility
        self.daily_vol = ml.util.get_daily_vol(
            close=self.data['close'], lookback=lookback)

        # Apply Symmetric CUSUM Filter and get timestamps for events
        # Note: Only the CUSUM filter needs a point estimate for volatility
        self.cusum_events = ml.filters.cusum_filter(
            self.data['close'], threshold=self.daily_vol[self.start_date:].mean() * 0.1)
        # self.data['close'], threshold=self.daily_vol[self.start_date:self.end_date].mean() * 0.1)
    # 9 triple barrier
    def triple_barrier(self, pt_sl=[0, 2], min_ret=0.0005, num_days=1):
        self.vertical_barriers = ml.labeling.add_vertical_barrier(
            t_events=self.cusum_events, close=self.data['close'], num_days=num_days)
        print(self.data['side'])
        print(pt_sl,min_ret,num_days)
        self.triple_barrier_events = ml.labeling.get_events(close=self.data['close'],
                                                            t_events=self.cusum_events,
                                                            pt_sl=pt_sl,
                                                            target=self.daily_vol,
                                                            min_ret=min_ret,
                                                            num_threads=2,
                                                            vertical_barrier_times=self.vertical_barriers,
                                                            side_prediction=self.data['side'])
        self.label = ml.labeling.get_bins(
            self.triple_barrier_events, self.data['close'])
        # self.label.to_csv('./data_mean_reverting/label.csv')
    # 10
    def features(self, fast_window=7, slow_window=15):
        # Log Returns
        self.raw_data['log_ret'] = np.log(self.raw_data['close']).diff()

        # Momentum
        self.raw_data['mom1'] = self.raw_data['close'].pct_change(periods=1)
        self.raw_data['mom2'] = self.raw_data['close'].pct_change(periods=2)
        self.raw_data['mom3'] = self.raw_data['close'].pct_change(periods=3)
        self.raw_data['mom4'] = self.raw_data['close'].pct_change(periods=4)
        self.raw_data['mom5'] = self.raw_data['close'].pct_change(periods=5)

        # Volatility
        window_stdev = 50
        self.raw_data['volatility'] = self.raw_data['log_ret'].rolling(
            window=window_stdev, min_periods=window_stdev, center=False).std()
        # Serial Correlation (Takes about 4 minutes)
        window_autocorr = 50
        self.raw_data['autocorr_1'] = self.raw_data['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=1), raw=False)
        self.raw_data['autocorr_2'] = self.raw_data['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=2), raw=False)
        self.raw_data['autocorr_3'] = self.raw_data['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=3), raw=False)
        self.raw_data['autocorr_4'] = self.raw_data['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=4), raw=False)
        self.raw_data['autocorr_5'] = self.raw_data['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=5), raw=False)

        # Get the various log -t returns
        self.raw_data['log_t1'] = self.raw_data['log_ret'].shift(1)
        self.raw_data['log_t2'] = self.raw_data['log_ret'].shift(2)
        self.raw_data['log_t3'] = self.raw_data['log_ret'].shift(3)
        self.raw_data['log_t4'] = self.raw_data['log_ret'].shift(4)
        self.raw_data['log_t5'] = self.raw_data['log_ret'].shift(5)

        # Add fast and slow moving averages

        self.raw_data['fast_mavg'] = self.raw_data['close'].rolling(
            window=fast_window, min_periods=fast_window, center=False).mean()
        self.raw_data['slow_mavg'] = self.raw_data['close'].rolling(
            window=slow_window, min_periods=slow_window, center=False).mean()

        # Add Trending signals
        self.raw_data['sma'] = np.nan

        long_signals = self.raw_data['fast_mavg'] >= self.raw_data['slow_mavg']
        short_signals = self.raw_data['fast_mavg'] < self.raw_data['slow_mavg']
        self.raw_data.loc[long_signals, 'sma'] = 1
        self.raw_data.loc[short_signals, 'sma'] = -1

        # Re compute sides
        self.raw_data['side'] = np.nan

        long_signals = self.raw_data['close'] <= self.raw_data['lower']
        short_signals = self.raw_data['close'] >= self.raw_data['upper']

        self.raw_data.loc[long_signals, 'side'] = 1
        self.raw_data.loc[short_signals, 'side'] = -1

        # Remove look ahead bias
        self.raw_data = self.raw_data.shift(1)
        # self.raw_data.to_csv('./data_mean_reverting/raw_data_features.csv')
        self.raw_data = self.raw_data.dropna()
        # Drop the NaN values from our data set
    # 11

    def split_dataset(self, test_size=0.2):

        # Get features at event dates
        self.X = self.raw_data.loc[self.label.index, :]
        # Drop unwanted columns
        # 'cum_buy_volume', 'cum_dollar_value'
        self.X.drop(['avg', 'upper', 'lower', 'open', 'high', 'low', 'close', 'cum_dollar_value',
                     'cum_buy_volume', 'cum_ticks', 'fast_mavg', 'slow_mavg', ], axis=1, inplace=True)

        if "Unnamed: 0" in self.X.columns.values:
            self.X.drop(["Unnamed: 0"], axis=1, inplace=True)
        if "tick_num" in self.X.columns.values:
            self.X.drop(["tick_num"], axis=1, inplace=True)
        self.y = self.label['bin']
        self.X.dropna(axis=0, how='any', inplace=True)
        self.y = self.y.loc[self.X.index]
        # Split data into training, validation and test sets
        self.X_training_validation = self.X[self.start_date:self.end_date]
        self.y_training_validation = self.y[self.start_date:self.end_date]
        self.X_train, self.X_validate, self.y_train, self.y_validate = train_test_split(
            self.X_training_validation, self.y_training_validation, test_size=test_size, shuffle=False)
        self.train_df = pd.concat(
            [self.y_train, self.X_train], axis=1, join='inner')

        # Upsample the training data to have a 50 - 50 split
        # https://elitedatascience.com/imbalanced-classes
        majority = self.train_df[self.train_df['bin'] == 0]
        minority = self.train_df[self.train_df['bin'] == 1]

        new_minority = resample(minority,
                                replace=True,     # sample with replacement
                                # to match majority class
                                n_samples=majority.shape[0],
                                random_state=42)

        self.train_df = pd.concat([majority, new_minority])
        self.train_df = shuffle(self.train_df, random_state=42)
        # Create training data
        self.y_train = self.train_df['bin']
        self.X_train = self.train_df.loc[:, self.train_df.columns != 'bin']
        self.parameters = {'max_depth': [2, 3, 4, 5, 7],
                           'n_estimators': [1, 10, 25, 50, 100, 256, 512],
                           'random_state': [42]}

    def perform_grid_search(self):
        rf = RandomForestClassifier(criterion='entropy')

        clf = GridSearchCV(rf, self.parameters, cv=4,
                           scoring='roc_auc', n_jobs=3)

        clf.fit(self.X_train, self.y_train)
        # clf.cv_results_['mean_test_score'],
        return (clf.best_params_['n_estimators'], clf.best_params_['max_depth'])
    # 13

    def train(self):
        # Random Forest Model
        # print("~None: ", np.where(np.isnan(self.X_train['side'])))
        # return
        n_estimator, depth = self.perform_grid_search()
        c_random_state = 42
        self.rf = RandomForestClassifier(max_depth=depth, n_estimators=n_estimator,
                                         criterion='entropy', random_state=c_random_state)
        self.rf.fit(self.X_train, self.y_train.values.ravel())

    # 14
    def performance_matrics_accuracy(self, outfile='accuracy.png'):
        # Performance Metrics
        y_pred_rf = self.rf.predict_proba(self.X_validate)[:, 1]
        self.y_pred = self.rf.predict(self.X_validate)
        fpr_rf, tpr_rf, _ = roc_curve(self.y_validate, y_pred_rf)

        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr_rf, tpr_rf, label='RF')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.savefig(outfile)
        return (classification_report(self.y_validate, self.y_pred, output_dict=True), confusion_matrix(self.y_validate, self.y_pred), accuracy_score(self.y_validate, self.y_pred))

    def feature_importance(self, outfile="feature_importance.png"):
        # Feature Importance
        title = 'Feature Importance:'
        figsize = (15, 5)

        feat_imp = pd.DataFrame({'Importance': self.rf.feature_importances_})
        feat_imp['feature'] = self.X.columns
        feat_imp.sort_values(by='Importance', ascending=False, inplace=True)
        feat_imp = feat_imp

        feat_imp.sort_values(by='Importance', inplace=True)
        feat_imp = feat_imp.set_index('feature', drop=True)
        feat_imp.plot.barh(title=title, figsize=figsize)
        plt.xlabel('Feature Importance Score')
        plt.savefig(outfile)

    def get_daily_returns(self, intraday_returns):
        """
        This changes returns into daily returns that will work using pyfolio. Its not perfect...
        """
        # cum_rets = ((0.998001*(intraday_returns + 1)).cumprod())
        self.return_history = intraday_returns
        cum_rets = ((intraday_returns + 1).cumprod())
        # Downsample to daily
        daily_rets = cum_rets.resample('B').last()

        # Forward fill, Percent Change, Drop NaN
        daily_rets = daily_rets.ffill().pct_change().dropna()

        return daily_rets

    def performance_in_sample(self, outfile='performance_in_sample.png'):
        perf_func = pf.timeseries.perf_stats
        test_dates = self.X_validate.index
        meta_returns = self.label.loc[test_dates, 'ret'] * self.y_pred
        daily_meta_rets = self.get_daily_returns(meta_returns)

        # save the KPIs in a dataframe
        perf_stats_all = perf_func(returns=daily_meta_rets,
                                   factor_returns=None,
                                   positions=None,
                                   transactions=None,
                                   turnover_denom="AGB")

        self.perf_stats_df = pd.DataFrame(
            data=perf_stats_all, columns=['Meta Model'])

        # pf.create_returns_tear_sheet(meta_returns, benchmark_rets=None)
        pf.show_perf_stats(daily_meta_rets)
        plt.savefig(outfile)

    def performance_out_sample(self, outfile="performance_out_sample.png"):
        # extarct data for out-of-sample (OOS)
        perf_func = pf.timeseries.perf_stats
        X_oos = self.X[self.test_date:]
        y_oos = self.y[self.test_date:]

        y_pred_rf = self.rf.predict_proba(X_oos)[:, 1]
        y_pred = self.rf.predict(X_oos)

        fpr_rf, tpr_rf, _ = roc_curve(y_oos, y_pred_rf)
        test_dates = X_oos.index

        meta_returns = self.label.loc[test_dates, 'ret'] * y_pred
        daily_rets_meta = self.get_daily_returns(meta_returns)

        # save the KPIs in a dataframe
        perf_stats_all = perf_func(returns=daily_rets_meta,
                                   factor_returns=None,
                                   positions=None,
                                   transactions=None,
                                   turnover_denom="AGB")

        self.perf_stats_df['Meta Model OOS'] = perf_stats_all

        pf.create_returns_tear_sheet(daily_rets_meta, benchmark_rets=None)
        plt.savefig(outfile)

        return (classification_report(y_oos, y_pred, output_dict=True), confusion_matrix(y_oos, y_pred), accuracy_score(y_oos, y_pred), self.perf_stats_df)

    def return_history_csv(self, outfil):
        self.return_history.to_csv(outfil)

    def save_model(self, outfile="model"):
        outfile += ".joblib"
        dump(self.rf, outfile)
