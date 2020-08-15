import mlfinlab as ml
import matplotlib.pyplot as plt
import pandas as pd


class Filter_label:
    def __init__(self, inputFile=None,df=None):
        if inputFile:
            self.df = pd.read_csv(inputFile, index_col=0)
            self.df.index = pd.to_datetime(self.df.date_time)
            self.df.drop(columns=['date_time'], inplace=True)
        else:
            self.df = df 

    def get_df(self):
        return self.df
    """
    cusum_fitler: return filtered dataframe
    input: df, lookback
    """

    def cusum_filter(self, lookback=50):
        if not len(self.df):
            print("data not defined")
            return
        self.daily_vol = ml.util.get_daily_vol(
            close=self.df['close'], lookback=lookback)
        self.cusum_events = ml.filters.cusum_filter(
            self.df['close'], threshold=self.daily_vol.mean() * 0.1)

    def plot_cusum(self):
        df2 = self.df.loc[self.cusum_events]
        plt.plot(self.df.index, self.df['close'])
        plt.plot(df2.index, df2['close'], marker='o')
        plt.show()

    """
    plot daily vol 
    """

    def plot_daily_vol(self):
        dailyVol = ml.util.get_daily_vol(self.df['close'])
        f, ax = plt.subplots()
        dailyVol.plot(ax=ax)
        ax.axhline(dailyVol.mean(), ls='--', color='r')
        plt.show()

    def get_daily_vol(self):
        self.daily_vol = ml.util.get_daily_vol(
            close=self.df['close'], lookback=50)
        return self.daily_vol
    def triple_barrier(self, pt_sl=[1, 2], min_ret=0.0005, num_days=1, target=None, mannual=False, side=False):
        self.vertical_barriers = ml.labeling.add_vertical_barrier(
            t_events=self.cusum_events, close=self.df['close'], num_days=num_days)
        print('mannual: ', mannual, "side: ", side, "target: ", target)
        if not mannual:
            # self.daily_vol = self.daily_vol.to_frame()
            # self.daily_vol['close']=0.01
            # self.daily_vol = pd.Series(self.daily_vol['close'].values,index=self.daily_vol.index)
            self.triple_barrier_events = ml.labeling.get_events(close=self.df['close'],
                                                                t_events=self.cusum_events,
                                                                pt_sl=pt_sl,
                                                                target=self.daily_vol,
                                                                min_ret=min_ret,
                                                                num_threads=5,
                                                                vertical_barrier_times=self.vertical_barriers,
                                                                side_prediction=self.df['side'])
            self.label = ml.labeling.get_bins(
                self.triple_barrier_events, self.df['close'])
            return self.label
        elif target and not side:
            self.triple_barrier_events = ml.labeling.get_events(close=self.df['close'],
                                                                t_events=self.cusum_events,
                                                                pt_sl=pt_sl,
                                                                target=target,
                                                                min_ret=min_ret,
                                                                num_threads=2,
                                                                vertical_barrier_times=self.vertical_barriers)
            self.label = ml.labeling.get_bins(
                self.triple_barrier_events, self.df['close'])
            return self.label
        elif not target and not side:
            self.triple_barrier_events = ml.labeling.get_events(close=self.df['close'],
                                                                t_events=self.cusum_events,
                                                                pt_sl=pt_sl,
                                                                target=self.daily_vol,
                                                                min_ret=min_ret,
                                                                num_threads=2,
                                                                vertical_barrier_times=self.vertical_barriers)
            self.label = ml.labeling.get_bins(
                self.triple_barrier_events, self.df['close'])
            return self.label

    def triple_barrier_fix(self, pt_sl=[1, 2], min_ret=0.0005, num_days=1, target=None, mannual=False, side=False):
        self.vertical_barriers = ml.labeling.add_vertical_barrier(
            t_events=self.cusum_events, close=self.df['close'], num_days=num_days)
        print('mannual: ', mannual, "side: ", side, "target: ", target)
        if not mannual:
            self.daily_vol = self.daily_vol.to_frame()
            self.daily_vol['close']=target
            self.daily_vol = pd.Series(self.daily_vol['close'].values,index=self.daily_vol.index)
            self.triple_barrier_events = ml.labeling.get_events(close=self.df['close'],
                                                                t_events=self.cusum_events,
                                                                pt_sl=pt_sl,
                                                                target=self.daily_vol,
                                                                min_ret=min_ret,
                                                                num_threads=5,
                                                                vertical_barrier_times=self.vertical_barriers,
                                                                side_prediction=self.df['side'])
            self.label = ml.labeling.get_bins(
                self.triple_barrier_events, self.df['close'])
            return self.label
    def triple_barrier_fix_no_side(self, pt_sl=[1, 2], min_ret=0.0005, num_days=1, target=None, mannual=False, side=False):
        self.vertical_barriers = ml.labeling.add_vertical_barrier(
            t_events=self.cusum_events, close=self.df['close'], num_days=num_days)
        print('mannual: ', mannual, "side: ", side, "target: ", target)
        if not mannual:
            self.daily_vol = self.daily_vol.to_frame()
            self.daily_vol['close']=target
            self.daily_vol = pd.Series(self.daily_vol['close'].values,index=self.daily_vol.index)
            self.triple_barrier_events = ml.labeling.get_events(close=self.df['close'],
                                                                t_events=self.cusum_events,
                                                                pt_sl=pt_sl,
                                                                target=self.daily_vol,
                                                                min_ret=min_ret,
                                                                num_threads=5,
                                                                vertical_barrier_times=self.vertical_barriers)
            self.label = ml.labeling.get_bins(
                self.triple_barrier_events, self.df['close'])
            return self.label