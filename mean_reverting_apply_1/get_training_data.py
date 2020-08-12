import sys
sys.path.append("../mean_reverting")
import preprocess 

"""
outfile: ./name/
"""
def generate_training_dataset(outfile,inputfile,label_type="vol"):
    pre = preprocess.Preprocess(inputfile) 
    x_features = pre.x_features1()
    # feature only csv 
    path = outfile+"x_features.csv"
    x_features.to_csv(path)
    # lable csv 
    label = None 
    if label_type =="vol":
        path = outfile+"label_vol.csv"
        label = pre.label_vol()
        label.to_csv(path)
    elif label_type == "fix": 
        path = outfile+"label_fix.csv"
        label = pre.label_fix() 
        label.to_csv(path)
    else:
        print("label_type undefined")
        return 

    # clean 
    x_features = pre.clean_df() 

    # add features to labels 
    x_features = x_features.loc[label.index,:]
    features = ['mom1', 'mom2', 'mom3', 'mom4', 'mom5',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4',
       'autocorr_5', 'log_t1', 'log_t2', 'log_t3', 'log_t4', 'log_t5', 'log_ret','volatility','rsi']
    # drop all non-feature columns 
    x_y = x_features[features]
    path = outfile +"x_y"
    x_y.to_csv(path)