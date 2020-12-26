import mlfinlab as ml
import numpy as np
import pandas as pd
import pyfolio as pf
import timeit

from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, classification_report, confusion_matrix, accuracy_score
from sklearn.utils import resample
from sklearn.utils import shuffle

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold

from mlfinlab.feature_importance import mean_decrease_impurity, mean_decrease_accuracy, single_feature_importance, plot_feature_importance
from mlfinlab.ensemble import SequentiallyBootstrappedBaggingClassifier
from mlfinlab.sample_weights import get_weights_by_return, get_weights_by_time_decay

from sklearn import datasets
from joblib import dump, load

import matplotlib.pyplot as plt


class Trend_following_weights:
    # "start_date format: 2016-01-06"
    # start and end date for training set
    def __init__(self, dataFile):
        self.data = self.read_data(dataFile)

    def read_data(self, fileName):
        # 1 Read in data
        if not fileName:
            print("invalid file - read_data")
            return
        print("---------")
        print(fileName)
        print('\n')
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

    def move_average(self, fast=7, slow=25):
        # 2 compute moving averages
        fast_window = fast
        slow_window = slow
        self.data['fast_mavg'] = self.data['close'].rolling(
            window=fast_window, min_periods=fast_window, center=False).mean()
        self.data['slow_mavg'] = self.data['close'].rolling(
            window=slow_window, min_periods=slow_window, center=False).mean()

    def bid_side(self):
        # Compute sides
        self.data['side'] = np.nan
        long_signals = self.data['fast_mavg'] >= self.data['slow_mavg']
        short_signals = self.data['fast_mavg'] < self.data['slow_mavg']
        self.data.loc[long_signals, 'side'] = 1
        self.data.loc[short_signals, 'side'] = -1
        # Remove Look ahead biase by lagging the signal
        self.data['side'] = self.data['side'].shift(1)
        self.raw_data = self.data.copy()
        # Drop the NaN values from our data set
        self.data.dropna(axis=0, how='any', inplace=True)

    def daily_volatility(self, lookback=50):
        # 3 Compute daily volatility
        self.daily_vol = ml.util.get_daily_vol(
            close=self.data['close'], lookback=lookback)
        # Apply Symmetric CUSUM Filter and get timestamps for events
        # Note: Only the CUSUM filter needs a point estimate for volatility
        self.cusum_events = ml.filters.cusum_filter(
            self.data['close'], threshold=self.daily_vol[self.start_date:].mean()*0.5)

    def triple_barrier(self, pt_sl=[1.5, 1], min_ret=0.005, num_days=1):
        # 4 triple barrier
        # Compute vertical barrier
        self.vertical_barriers = ml.labeling.add_vertical_barrier(
            t_events=self.cusum_events, close=self.data['close'], num_days=1)
        self.triple_barrier_events = ml.labeling.get_events(close=self.data['close'],
                                                            t_events=self.cusum_events,
                                                            pt_sl=pt_sl,
                                                            target=self.daily_vol,
                                                            min_ret=min_ret,
                                                            num_threads=3,
                                                            vertical_barrier_times=self.vertical_barriers,
                                                            side_prediction=self.data['side'])

        self.labels = ml.labeling.get_bins(
            self.triple_barrier_events, self.data['close'])

    # add moving avergae, bid-size, daily volatility, triple_barrier to the data set
    def process_data(self, pt_sl=[1.5, 1], min_ret=0.005, num_days=1):
        self.move_average()
        self.bid_side()
        self.daily_volatility()
        self.triple_barrier(pt_sl, min_ret, num_days)

    def features(self):
        # 5 Log Returns
        self.raw_data['log_ret'] = np.log(self.raw_data['close']).diff()

        # Momentum
        self.raw_data['mom1'] = self.raw_data['close'].pct_change(periods=1)
        self.raw_data['mom2'] = self.raw_data['close'].pct_change(periods=2)
        self.raw_data['mom3'] = self.raw_data['close'].pct_change(periods=3)
        self.raw_data['mom4'] = self.raw_data['close'].pct_change(periods=4)
        self.raw_data['mom5'] = self.raw_data['close'].pct_change(periods=5)

        # Volatility
        self.raw_data['volatility_50'] = self.raw_data['log_ret'].rolling(
            window=50, min_periods=50, center=False).std()
        self.raw_data['volatility_31'] = self.raw_data['log_ret'].rolling(
            window=31, min_periods=31, center=False).std()
        self.raw_data['volatility_15'] = self.raw_data['log_ret'].rolling(
            window=15, min_periods=15, center=False).std()

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
        # Re compute sides
        self.raw_data['side'] = np.nan

        long_signals = self.raw_data['fast_mavg'] >= self.raw_data['slow_mavg']
        short_signals = self.raw_data['fast_mavg'] < self.raw_data['slow_mavg']

        self.raw_data.loc[long_signals, 'side'] = 1
        self.raw_data.loc[short_signals, 'side'] = -1
        self.raw_data = self.raw_data.shift(1)
        self.raw_data.dropna(axis=0, how='any', inplace=True)

    def training_dataset(self, outfile):
        # 6 Get features at event dates
        self.X = self.raw_data.loc[self.labels.index, :]

        # Drop unwanted columns
        # cum_dollar_value','cum_ticks' cum_buy_volume
        self.X.drop(['open', 'high', 'low', 'close', 'cum_buy_volume', 'cum_dollar_value',
                     'cum_ticks', 'fast_mavg', 'slow_mavg', "volume"], axis=1, inplace=True)
        if "Unnamed: 0" in self.X.columns.values:
            self.X.drop(["Unnamed: 0"], axis=1, inplace=True)
        if "tick_num" in self.X.columns.values:
            self.X.drop(["tick_num"], axis=1, inplace=True)

        self.X.dropna(axis=0, how='any', inplace=True)

        self.X.to_csv(outfile+"_features.csv")
        self.y = self.labels['bin']
        self.y = self.y.loc[self.X.index]
        # 7 Split data into training, validation and test sets
        self.X_training_validation = self.X[self.start_date:self.end_date]
        self.y_training_validation = self.y[self.start_date:self.end_date]
        self.X_train, self.X_validate, self.y_train, self.y_validate = train_test_split(
            self.X_training_validation, self.y_training_validation, test_size=0.15, shuffle=False)

        # self.train_df = pd.concat(
        #     [self.y_train, self.X_train], axis=1, join='inner')
        # majority = self.train_df[self.train_df['bin'] == 0]
        # minority = self.train_df[self.train_df['bin'] == 1]
        # majority = self.train_df[self.train_df['bin'] == 0]
        # minority = self.train_df[self.train_df['bin'] == 1]

        # new_minority = resample(minority,
        #                         replace=True,     # sample with replacement
        #                         # to match majority class
        #                         n_samples=majority.shape[0],
        #                         random_state=42)

        # self.train_df = pd.concat([majority, new_minority])
        # self.train_df = shuffle(self.train_df, random_state=42)

        # # Create training data
        # self.y_train = self.train_df['bin']
        # self.X_train = self.train_df.loc[:, self.train_df.columns != 'bin']

    def sample_weights(self):
        self.return_based_sample_weights = get_weights_by_return(
            self.triple_barrier_events.loc[self.X_train.index], self.data.loc[self.X_train.index, 'close'])
        # self.time_based_sample_weights = get_weights_by_time_decay(
        #     self.triple_barrier_events.loc[self.X_train.index], self.data.loc[self.X_train.index, 'close'], decay=0.5)
        # self.return_based_sample_weights.plot()
        # plt.savefig('sample_weight.png')
    # def cross_validation(self):
    #     self.parameters = {'max_depth': [2, 3, 4, 5, 7],
    #                        'n_estimators': [10, 25, 50, 100, 256, 512]}
    #     self.cv_gen_standard = KFold(4)
    #     self.cv_gen_purged = ml.cross_validation.PurgedKFold(n_splits=4,
    #                                                          samples_info_sets=self.triple_barrier_events.loc[self.X_train.index].t1)

    # 8
    def perform_grid_search(self, cv_gen, scoring):
        """
        Grid search using Purged CV without using sample weights in fit(). Returns top model and top score
        """
        self.parameters = {'max_depth': [2, 3, 4, 5, 7],
                           'n_estimators': [10, 25, 50, 100, 256, 512]}
        self.cv_gen_standard = KFold(4)
        self.cv_gen_purged = ml.cross_validation.PurgedKFold(n_splits=4,
                                                             samples_info_sets=self.triple_barrier_events.loc[self.X_train.index].t1)
        max_cross_val_score = -np.inf
        top_model = None
        for m_depth in self.parameters['max_depth']:
            for n_est in self.parameters['n_estimators']:
                clf_base = DecisionTreeClassifier(criterion='entropy', random_state=42,
                                                  max_depth=m_depth, class_weight='balanced')
                if type == 'standard':
                    clf = BaggingClassifier(n_estimators=n_est,
                                            base_estimator=clf_base,
                                            random_state=42, n_jobs=-1,
                                            oob_score=False, max_features=1.)
                elif type == 'random_forest':
                    clf = RandomForestClassifier(n_estimators=n_est,
                                                 max_depth=m_depth,
                                                 random_state=42,
                                                 n_jobs=-1,
                                                 oob_score=False,
                                                 criterion='entropy',
                                                 class_weight='balanced_subsample',
                                                 max_features=1.)
                elif type == 'sequential_bootstrapping':
                    clf = SequentiallyBootstrappedBaggingClassifier(samples_info_sets=self.triple_barrier_events.loc[self.X_train.index].t1,
                                                                    price_bars=data.loc[self.X_train.index.min(
                                                                    ):self.X_train.index.max(), 'close'],
                                                                    n_estimators=n_est, base_estimator=clf_base,
                                                                    random_state=42, n_jobs=-1, oob_score=False,
                                                                    max_features=1.)
                temp_score_base = ml.cross_validation.ml_cross_val_score(
                    clf, self.X_train, self.y_train, cv_gen, scoring=scoring)
                if temp_score_base.mean() > max_cross_val_score:
                    max_cross_val_score = temp_score_base.mean()
                    # print(temp_score_base.mean())
                    top_model = clf
        return top_model, max_cross_val_score
        # rf = RandomForestClassifier(criterion='entropy')

        # clf = GridSearchCV(rf, self.parameters, cv=4,
        #                    scoring='roc_auc', n_jobs=3)

        # clf.fit(self.X_train, self.y_train)
        # # clf.cv_results_['mean_test_score'],
        # return (clf.best_params_['n_estimators'], clf.best_params_['max_depth'])

    def perform_grid_search_sample_weights(self, scoring='f1', type='standard'):
        """
        Grid search using Purged CV using sample weights in fit(). Returns top model and top score
        """
        self.parameters = {'max_depth': [2, 3, 4, 5, 7],
                           'n_estimators': [10, 25, 50, 100, 256, 512]}
        self.cv_gen_purged = ml.cross_validation.PurgedKFold(n_splits=4,
                                                             samples_info_sets=self.triple_barrier_events.loc[self.X_train.index].t1)
        max_cross_val_score = -np.inf
        top_model = None
        for m_depth in self.parameters['max_depth']:
            for n_est in self.parameters['n_estimators']:
                clf_base = DecisionTreeClassifier(criterion='entropy', random_state=42,
                                                  max_depth=m_depth, class_weight='balanced')
                if type == 'standard':
                    clf = BaggingClassifier(n_estimators=n_est,
                                            base_estimator=clf_base,
                                            random_state=42, n_jobs=-1,
                                            oob_score=False, max_features=1.)
                elif type == 'random_forest':
                    clf = RandomForestClassifier(n_estimators=n_est,
                                                 max_depth=m_depth,
                                                 random_state=42,
                                                 n_jobs=-1,
                                                 oob_score=False,
                                                 criterion='entropy',
                                                 class_weight='balanced_subsample',
                                                 max_features=1.)
                elif type == 'sequential_bootstrapping':
                    clf = SequentiallyBootstrappedBaggingClassifier(samples_info_sets=self.triple_barrier_events.loc[self.X_train.index].t1,
                                                                    price_bars=self.data.loc[self.X_train.index.min(
                                                                    ):self.X_train.index.max(), 'close'],
                                                                    n_estimators=n_est, base_estimator=clf_base,
                                                                    random_state=42, n_jobs=-1, oob_score=False,
                                                                    max_features=1.)
                self.X_train.to_csv("x_train_debug.csv")
                temp_score_base = ml.cross_validation.ml_cross_val_score(
                    clf, self.X_train, self.y_train, self.cv_gen_purged, sample_weight_train=self.return_based_sample_weights.values, scoring=accuracy_score)
                if temp_score_base.mean() > max_cross_val_score:
                    self.max_cross_val_score = temp_score_base.mean()
                    self.top_model = clf

    def feature_importance(self, outfile):
        mdi_feat_imp = mean_decrease_impurity(
            self.top_model, self.X_train.columns)
        plot_feature_importance(mdi_feat_imp, 0, 0)
        plt.savefig(outfile)

    def performance_metrics(self):
        # 10 Performance Metrics
        y_pred_rf = self.top_model.predict_proba(self.X_train)[:, 1]
        self.y_pred = self.top_model.predict(self.X_train)
        fpr_rf, tpr_rf, _ = roc_curve(self.y_train, y_pred_rf)
        return classification_report(self.y_train, self.y_pred, output_dict=True), accuracy_score(self.y_train, self.y_pred)

    def performance_metrics_meta(self):
        # 11 Meta-label
        # Performance Metrics
        y_pred_rf = self.top_model.predict_proba(self.X_validate)[:, 1]
        self.y_pred = self.top_model.predict(self.X_validate)
        fpr_rf, tpr_rf, _ = roc_curve(self.y_validate, y_pred_rf)
        return (confusion_matrix(self.y_validate, self.y_pred), accuracy_score(self.y_validate, self.y_pred), classification_report(self.y_validate, self.y_pred, output_dict=True))

    # def plot_metrics_meta(self, fpr_rf, tpr_rf, outputfile="plot_metrics_meta.png"):
    #     plt.figure(1)
    #     plt.plot([0, 1], [0, 1], 'k--')
    #     plt.plot(fpr_rf, tpr_rf, label='RF')
    #     plt.xlabel('False positive rate')
    #     plt.ylabel('True positive rate')
    #     plt.title('ROC curve')
    #     plt.legend(loc='best')
    #     plt.savefig(outputfile)

    # def feature_importance_image(self, outputfile="feature_importance_image.png", outputfile2="feature_importance_image2.png"):
    #     # 12 Feature Importance

    #     # MDI, MDA, SFI feature importance
    #     plot_feature_importance
    #     mdi_feat_imp = mean_decrease_impurity(
    #         self.top_model, self.X_train.columns)
    #     mda_feat_imp = mean_decrease_accuracy(self.top_model, self.X_train, self.y_train, self.cv_gen_purged, scoring='f1',
    #                                           sample_weight_train=self.return_based_sample_weights.values)
    #     sfi_feat_imp = single_feature_importance(self.top_model, self.X_train, self.y_train, self.cv_gen_purged, scoring='f1',
    #                                              sample_weight_train=self.return_based_sample_weights.values)
    #     plot_feature_importance(mdi_feat_imp, 0, 0)
    #     plt.savefig(outputfile)
    #     plot_feature_importance(mda_feat_imp, 0, 0)
    #     plt.savefig(outputfile2)

    def get_daily_returns(self, intraday_returns, f="return_history_trend_following_weights.csv"):
        """
        This changes returns into daily returns that will work using pyfolio. Its not perfect...
        """
        # cum_rets = ((0.998001*(intraday_returns + 1)).cumprod())
        cum_rets = ((intraday_returns + 1).cumprod())
        # Downsample to daily
        daily_rets = cum_rets.resample('B').last()

        # Forward fill, Percent Change, Drop NaN
        daily_rets = daily_rets.ffill().pct_change().dropna()

        return daily_rets

    def validation_metrics(self):
        # 14
        valid_dates = self.X_validate.index
        meta_returns = self.labels.loc[valid_dates, 'ret'] * self.y_pred
        daily_meta_rets = self.get_daily_returns(meta_returns)
        perf_func = pf.timeseries.perf_stats
        # Save the statistics in a dataframe
        perf_stats_all = perf_func(returns=daily_meta_rets,
                                   factor_returns=None,
                                   positions=None,
                                   transactions=None,
                                   turnover_denom="AGB")
        self.perf_stats_df = pd.DataFrame(
            data=perf_stats_all, columns=['Meta Model'])

        return daily_meta_rets

    def test_out_of_sampe(self, outputImagePath="test_out_of_sampe_performance.png", kpiImagePath="test_out_of_kpi.png"):
        # 15 Extarct data for out-of-sample (OOS)
        X_oos = self.X[self.test_date:]
        y_oos = self.y[self.test_date:]
        # Performance Metrics
        y_pred_rf = self.top_model.predict_proba(X_oos)[:, 1]
        y_pred = self.top_model.predict(X_oos)
        fpr_rf, tpr_rf, _ = roc_curve(y_oos, y_pred_rf)

        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr_rf, tpr_rf, label='RF')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.savefig(outputImagePath)

        test_dates = X_oos.index
        meta_returns = self.labels.loc[test_dates, 'ret'] * y_pred
        daily_rets_meta = self.get_daily_returns(meta_returns)
        perf_func = pf.timeseries.perf_stats
        # save the KPIs in a dataframe
        perf_stats_all = perf_func(returns=daily_rets_meta,
                                   factor_returns=None,
                                   positions=None,
                                   transactions=None,
                                   turnover_denom="AGB")
        self.perf_stats_df['Meta Model OOS'] = perf_stats_all
        self.return_history = daily_rets_meta
        pf.create_returns_tear_sheet(daily_rets_meta, benchmark_rets=None)
        plt.savefig(kpiImagePath)
        return (confusion_matrix(y_oos, y_pred), accuracy_score(y_oos, y_pred), classification_report(y_oos, y_pred, output_dict=True), self.perf_stats_df)

    def return_history_csv(self, outfil):
        self.return_history.to_csv(outfil)

    def save_model(self, outfile="model"):
        outfile += ".joblib"
        dump(self.top_model, outfile)
