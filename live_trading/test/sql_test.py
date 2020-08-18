import sys 
sys.path.append('../handle_sql')
import preprocess_sql as ps 
pairs = ["BTCUSDT","ETHUSDT","IOTAUSDT"]
for p in pairs:
    p = ps.Preprocess_sql('../pair_db/features.sqlite',p)
    r = p.get_last_n(2)
    # r['index'] = r['index']+1 
    # r.index = r['index']
    # r.drop(columns=['index'],inplace=True)
    # r['tick_num']=1
    print(r.head())
    # p.store_df(r)
    # p.select_index()