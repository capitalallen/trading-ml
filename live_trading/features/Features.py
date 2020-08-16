
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
        rsi_df = self.get_rsi(self.data, window=window)
        self.data['rsi'] = pd.Series(data=rsi_df.values, index=self.data.index)