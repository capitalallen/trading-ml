"""
preprocessing 

constructor
    -> read raw data to df 
"""

"""
x_features1
    add features 
"""
import sys
sys.path.append("../labeling")
from features import Features
import pandas as pd 
import seaborn as sns
import filter_label
class Preprocess:
    def __init__(self,inputfile):
        self.df = pd.read_csv(inputfile, index_col=0)
        self.df['date_time'] = pd.to_datetime(self.df.date_time)
        self.f = Features()
    def x_features1(self):
        self.df = self.f.add_bbands(self.df)
        self.df = self.f.compute_side(self.df)
        self.df = self.f.add_momantum(self.df)
        self.df = self.f.add_volatility(self.df)
        self.df = self.f.add_serial_correlation(self.df)
        self.df = self.f.add_log_returns(self.df)
        self.df = self.f.mov_average(self.df)
        self.df = self.f.add_rsi(self.df)
        self.df = self.f.add_kdj(self.df)
        self.df = self.f.add_trending_signal(self.df)
        return self.df
    
    def clean_df(self):
        self.df.dropna(axis=0, how='any', inplace=True)
        return self.df

    """
    print highly correlated pairs 
    """ 
    def correlation(self,corr_matrix=0.6):
        corr_matrix = self.df.corr().abs()
        high_corr_var=np.where(corr_matrix>0.6)
        high_corr_var=[(corr_matrix.columns[x],corr_matrix.columns[y]) for x,y in zip(*high_corr_var) if x!=y and x<y]
        print(high_corr_var)
    
    def check_null(self):
        print(self.df.isnull().sum())
        sns.heatmap(self.df.isnull(),cmap="viridis")
        plt.show()
    
    def labeling(self,df=None):
        fl = None
        if df.shape[0]!=0:
            fl = filter_label.Filter_label(df=df)
            fl.cusum_filter()        
        else:
            fl = filter_label.Filter_label(df=self.df)
            fl.cusum_filter()
        return fl.triple_barrier()
    
    """
    label dataset based on vol 
    """
    def label_vol(self):
        fl = filter_label.Filter_label(df=self.df)
        fl.cusum_filter()
        return fl.triple_barrier()    
    
    """
    label dataset based on target 
    """
    def label_fix(self,target = 0.01):
        fl = filter_label.Filter_label(df=self.df)
        fl.cusum_filter()
        return fl.triple_barrier_fix(target=target)    