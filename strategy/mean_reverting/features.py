import pandas as pd
from finta import TA
import numpy as np


class Features:

    def __init__(self):
        pass

    """
    rsi 
    """

    def rsi(self, df, n):
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
        if 'date_time' in df.columns:
            rsi_df = pd.Series(data=RSI.values, index=df.date_time)
        else:
            rsi_df = pd.Series(data=RSI.values, index=df.index)
        return rsi_df

    def add_rsi(self, df, window=14):
        df['rsi'] = self.rsi(df,n=window).values
        return df

    def srsi(self, df):
        st = TA.STOCHRSI(df)
        st = st*100
        sch_rsi = None
        if 'date_time' in df.columns:
            sch_rsi = pd.Series(data=st.values, index=df.date_time)
        else:
            sch_rsi = pd.Series(data=st.values, index=df.index)
        return sch_rsi

    def add_srsi(self, df):
        st = TA.STOCHRSI(df)
        st = st*100
        df['srsi'] = self.srsi(df).values
        return df

    def CCI(self, df):
        cci = TA.CCI(df)
        cci = cci*100
        cci_series = None
        if 'date_time' in df.columns:
            cci_series = pd.Series(data=cci.values, index=df.date_time)
        else:
            cci_series = pd.Series(data=cci.values, index=df.index)
        return cci_series

    def add_cci(self, df):
        cci = TA.CCI(df)
        df['cci'] = cci.values
        return df

    def williams(self, df):
        will = TA.WILLIAMS(df)
        will = will*100
        will_series = None
        if 'date_time' in df.columns:
            will_series = pd.Series(data=will.values, index=df.date_time)
        else:
            will_series = pd.Series(data=will.values, index=df.index)
        return will_series

    def add_williams(self, df):
        will = TA.WILLIAMS(df)
        df['williams'] = will.values
        return df

    def bbands(self, close_prices, window=21, no_of_stdev=1.5):
        # rolling_mean = close_prices.rolling(window=window).mean()
        # rolling_std = close_prices.rolling(window=window).std()
        rolling_mean = close_prices.ewm(span=window).mean()
        rolling_std = close_prices.ewm(span=window).std()

        upper_band = rolling_mean + (rolling_std * no_of_stdev)
        lower_band = rolling_mean - (rolling_std * no_of_stdev)

        return rolling_mean, upper_band, lower_band

    def add_bbands(self, data, window=21, no_of_stdev=1.5):
        data['avg'], data['upper'], data['lower'] = self.bbands(
            data['close'], window, no_of_stdev=no_of_stdev)
        return data

    """
    compute side with bbands
    """

    def compute_side(self, df):
        # Compute sides
        df['side'] = np.nan

        long_signals = (df['close'] <= df['lower'])
        short_signals = (df['close'] >= df['upper'])

        df.loc[long_signals, 'side'] = 1
        df.loc[short_signals, 'side'] = -1

        # Remove Look ahead biase by lagging the signal
        df['side'] = df['side'].shift(1)
        return df
    """
    compute side with min value 
    """

    def compute_side_min(self, df):
        # Compute sides
        df['side'] = np.nan

        long_signals = (df['low'] <= df['lower'])
        short_signals = (df['high'] >= df['upper'])

        df.loc[long_signals, 'side'] = 1
        df.loc[short_signals, 'side'] = -1

        # Remove Look ahead biase by lagging the signal
        df['side'] = df['side'].shift(1)
        return df
    """
    add momantum 
    """

    def add_momantum(self, df):
        # Momentum
        df['mom1'] = df['close'].pct_change(periods=1)
        df['mom2'] = df['close'].pct_change(periods=2)
        df['mom3'] = df['close'].pct_change(periods=3)
        df['mom4'] = df['close'].pct_change(periods=4)
        df['mom5'] = df['close'].pct_change(periods=5)
        return df

    """
    add volatity
    """

    def add_volatility(self, df, window_stdev=50):
        if 'log_ret' not in df.columns:
            df['log_ret'] = np.log(df['close']).diff()
        df['volatility'] = df['log_ret'].rolling(
            window=window_stdev, min_periods=window_stdev, center=False).std()
        return df
    """
    add Serial Correlation
    """

    def add_serial_correlation(self, df, window_autocorr=50):
        if 'log_ret' not in df.columns:
            df['log_ret'] = np.log(df['close']).diff()
        window_autocorr = 50
        df['autocorr_1'] = df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=1), raw=False)
        df['autocorr_2'] = df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=2), raw=False)
        df['autocorr_3'] = df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=3), raw=False)
        df['autocorr_4'] = df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=4), raw=False)
        df['autocorr_5'] = df['log_ret'].rolling(
            window=window_autocorr, min_periods=window_autocorr, center=False).apply(lambda x: x.autocorr(lag=5), raw=False)
        return df

    """
    add log returns 
    """

    def add_log_returns(self, df):
        df['log_ret'] = np.log(df['close']).diff()
        # Get the various log -t returns
        df['log_t1'] = df['log_ret'].shift(1)
        df['log_t2'] = df['log_ret'].shift(2)
        df['log_t3'] = df['log_ret'].shift(3)
        df['log_t4'] = df['log_ret'].shift(4)
        df['log_t5'] = df['log_ret'].shift(5)
        return df

    """
    add fast and sloe moving averages 
    """

    def mov_average(self, df, fast_window=7, slow_window=15):
        # Add fast and slow moving averages
        df['fast_mavg'] = df['close'].rolling(
            window=fast_window, min_periods=fast_window, center=False).mean()
        df['slow_mavg'] = df['close'].rolling(
            window=slow_window, min_periods=slow_window, center=False).mean()
        return df

    """
    add trending signals 
    """

    def add_trending_signal(self, df):
        # Add Trending signals
        df['sma'] = np.nan

        long_signals = df['fast_mavg'] >= df['slow_mavg']
        short_signals = df['fast_mavg'] <= df['slow_mavg']
        df.loc[long_signals, 'sma'] = 1
        df.loc[short_signals, 'sma'] = -1
        return df

    """
    Stochastic oscillator
    """
    def add_kdj(self,df):
        k = TA.STOCH(df)
        d = TA.STOCHD(df)
        # if 'date_time' in df.columns:
        #     df['date_time'] = pd.to_datetime(df.date_time)
        #     df['kdj_k'] = pd.Series(data=k.values, index=df.date_time)
        #     df['kdj_d'] = pd.Series(data=d.values, index=df.date_time)
        # else:
        #     df.index = pd.to_datetime(df.index)
        #     df['kdj_k'] = pd.Series(data=k.values, index=df.index)
        #     df['kdj_d'] = pd.Series(data=d.values, index=df.index)
        df['kdj_k'] = k.values 
        df['kdj_d'] = d.values
        return df 