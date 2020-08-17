import preprocess_sql as ps 
import sync_sql as ss 
p = ps.Preprocess_sql('features.sqlite',"x_features")
r = p.get_last_n(2)
# r['index'] = r['index']+1 
# r.index = r['index']
# r.drop(columns=['index'],inplace=True)
# r['tick_num']=1
print(r.head())
# p.store_df(r)
# p.select_index()