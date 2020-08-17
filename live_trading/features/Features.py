import pandas as pd 
import numpy as np 
from finta import TA
class Features: 
    def __init__(self,df):
        self.df = df  
    
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

    def add_rsi(self, window=14):
        # Compute RSI
        rsi_df = self.get_rsi(self.df, window=window)
        self.df['rsi'] = pd.Series(data=rsi_df.values, index=self.df.index)

    def srsi(self, df):
        st = TA.STOCHRSI(df)
        st = st*100
        sch_rsi = None
        if 'date_time' in df.columns:
            sch_rsi = pd.Series(data=st.values, index=df.date_time)
        else:
            sch_rsi = pd.Series(data=st.values, index=df.index)
        return sch_rsi

    def add_srsi(self):
        st = TA.STOCHRSI(self.df)
        st = st*100
        self.df['srsi'] = self.srsi(self.df).values
    
    def bbands(self, close_prices, window=21, no_of_stdev=1.5):
        # rolling_mean = close_prices.rolling(window=window).mean()
        # rolling_std = close_prices.rolling(window=window).std()
        rolling_mean = close_prices.ewm(span=window).mean()
        rolling_std = close_prices.ewm(span=window).std()

        upper_band = rolling_mean + (rolling_std * no_of_stdev)
        lower_band = rolling_mean - (rolling_std * no_of_stdev)

        return rolling_mean, upper_band, lower_band

    def add_bbands(self, window=21, no_of_stdev=1.5):
        self.df['avg'], self.df['upper'], self.df['lower'] = self.bbands(
            self.df['close'], window, no_of_stdev=no_of_stdev)

    """
    compute side with bbands
    """

    def compute_side(self):
        # Compute sides
        self.df['side'] = np.nan

        long_signals = (self.df['close'] <= self.df['lower'])
        short_signals = (self.df['close'] >= self.df['upper'])

        self.df.loc[long_signals, 'side'] = 1
        self.df.loc[short_signals, 'side'] = -1

        # Remove Look ahead biase by lagging the signal
        self.df['side'] = self.df['side'].shift(1)
    """
    compute side with min value 
    """

    def compute_side_min(self):
        # Compute sides
        self.df['side'] = np.nan

        long_signals = (self.df['low'] <= self.df['lower'])
        short_signals = (self.df['high'] >= self.df['upper'])

        self.df.loc[long_signals, 'side'] = 1
        self.df.loc[short_signals, 'side'] = -1

        # Remove Look ahead biase by lagging the signal
        self.df['side'] = self.df['side'].shift(1)
    """
    add momantum 
    """

    def add_momantum(self):
        # Momentum
        self.df['mom1'] = self.df['close'].pct_change(periods=1)
        self.df['mom2'] = self.df['close'].pct_change(periods=2)
        self.df['mom3'] = self.df['close'].pct_change(periods=3)
        self.df['mom4'] = self.df['close'].pct_change(periods=4)
        self.df['mom5'] = self.df['close'].pct_change(periods=5)

    """
    add volatity
    """

    def add_volatility(self, window_stdev=50):
        if 'log_ret' not in self.df.columns:
            self.df['log_ret'] = np.log(self.df['close']).diff()
        self.df['volatility'] = self.df['log_ret'].rolling(
            window=window_stdev, min_periods=window_stdev, center=False).std()
    """
    add Serial Correlation
    """

    def add_serial_correlation(self,window_autocorr=50):
        if 'log_ret' not in self.df.columns:
            self.df['log_ret'] = np.log(self.df['close']).diff()
        window_autocorr = 50
        self.df['autocorr_1'] = self.df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=1), raw=False)
        self.df['autocorr_2'] = self.df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=2), raw=False)
        self.df['autocorr_3'] = self.df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=3), raw=False)
        self.df['autocorr_4'] = self.df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=4), raw=False)
        self.df['autocorr_5'] = self.df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=5), raw=False)
        return self.df

    """
    add log returns 
    """

    def add_log_returns(self):
        self.df['log_ret'] = np.log(self.df['close']).diff()
        # Get the various log -t returns
        self.df['log_t1'] = self.df['log_ret'].shift(1)
        self.df['log_t2'] = self.df['log_ret'].shift(2)
        self.df['log_t3'] = self.df['log_ret'].shift(3)
        self.df['log_t4'] = self.df['log_ret'].shift(4)
        self.df['log_t5'] = self.df['log_ret'].shift(5)

    """
    add fast and sloe moving averages 
    """

    def mov_average(self,fast_window=7, slow_window=15):
        # Add fast and slow moving averages
        self.df['fast_mavg'] = self.df['close'].rolling(
            window=fast_window, min_periods=fast_window, center=False).mean()
        self.df['slow_mavg'] = self.df['close'].rolling(
            window=slow_window, min_periods=slow_window, center=False).mean()

    """
    add trending signals 
    """

    def add_trending_signal(self):
        # Add Trending signals
        self.df['sma'] = np.nan

        long_signals = self.df['fast_mavg'] >= self.df['slow_mavg']
        short_signals = self.df['fast_mavg'] <= self.df['slow_mavg']
        self.df.loc[long_signals, 'sma'] = 1
        self.df.loc[short_signals, 'sma'] = -1
        return self.df
    
    def get_df(self):
        return self.df 
