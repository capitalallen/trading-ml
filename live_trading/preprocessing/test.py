import proprecess
import pandas as pd 
df = pd.read_csv('dol_bar.csv',index_col=0)
df.date_time = pd.to_datetime(df.date_time)
df1 = df.iloc[:20]
df2 = df.iloc[21:30]
print(df1.head())
print(df2.head())
print("------")
p = proprecess.Proprecessing()
p.combine_df(df1,df2)
p.add_features()
d1 = p.get_df2()
d2 = p.get_df2_test()
print(d1.head())
print(d2.head())
print(p.get_last_row(db_name='../handle_sql/features.sqlite',record_name="x_features"))