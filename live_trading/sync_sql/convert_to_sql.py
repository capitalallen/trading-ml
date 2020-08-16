from sqlalchemy import create_engine
import pandas as pd 
import sqlite3 
conn = sqlite3.connect('features.sqlite')
# cur = conn.cursor() 
# cur.execute('DROP TABLE IF EXISTS Tracks')
# cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER)')
df = pd.read_csv('x_features.csv',index_col=0)
df.date_time = pd.to_datetime(df.date_time)
df.to_sql('features', con=conn)
conn.close()
# engine = create_engine('sqlite://', echo=False)
# df = pd.read_csv('x_features.csv',index_col=0)
# df.date_time = pd.to_datetime(df.date_time)
# df.to_sql('features', con=engine)

def convert_to_sql(csv_file,db='features.sqlite',record="x_features.csv")