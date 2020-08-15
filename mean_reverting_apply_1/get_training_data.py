import sys
sys.path.append("../mean_reverting")
sys.path.append("../bar_generator")
sys.path.append("../data_downloader")
sys.path.append("../labeling")
import data_getter 
import filter_label
import bar_generate as bg 
import os 
import preprocess 
import pandas as pd 
"""
outfolder: ./name/
"""
# def generate_training_dataset(outfolder,inputfile,label_type="vol"):
#     pre = preprocess.Preprocess(inputfile) 
#     x_features = pre.x_features1()
    
#     # feature only csv 
#     path = outfolder+"x_features.csv"
#     x_features.to_csv(path)

#     # lable csv 
#     label = None 
#     if label_type =="vol":
#         path = outfolder+"label_vol.csv"
#         label = pre.label_vol()
#         label.to_csv(path)
#     elif label_type == "fix": 
#         path = outfolder+"label_fix.csv"
#         label = pre.label_fix() 
#         label.to_csv(path)
#     else:
#         print("label_type undefined")
#         return 

#     # clean 
#     x_features = pre.clean_df() 

#     # add features to labels 
#     x_features = x_features.loc[label.index,:]
#     features = ['mom1', 'mom2', 'mom3', 'mom4', 'mom5',
#        'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4',
#        'autocorr_5', 'log_t1', 'log_t2', 'log_t3', 'log_t4', 'log_t5', 'log_ret','volatility','rsi']
#     # drop all non-feature columns 
#     x_y = x_features[features]
#     path = outfolder +"x_y"
#     x_y.to_csv(path)

"""
convert daily_timebar and minut_timebar to dol_bar
"""
def get_dol_bar_30(outfolder,inputfile_daily="daily_timebar.csv",inputfile_min="minute_timebar.csv"):
    daily = pd.read_csv(outfolder+inputfile_daily)
    # minutes = pd.read_csv(outfolder+inputfile_min)
    daily_bar = bg.bar_generate(read_df=True,df=daily, outfolder=outfolder,outFile='daily_time.csv')
    daily_bar.cal_threshold("daily_av_50")
    threshold = daily_bar.get_threshold()

    generator = bg.bar_generate(inputFile=outfolder+inputfile_min,outFile="dol_bar.csv",outfolder=outfolder)
    generator.set_threshold(threshold)
    generator.convert_dol_bar()

def get_dol_bar_15(outfolder,inputfile_daily="daily_timebar.csv",inputfile_min="minute_timebar.csv"):
    daily = pd.read_csv(outfolder+inputfile_daily)
    # minutes = pd.read_csv(outfolder+inputfile_min)
    daily_bar = bg.bar_generate(read_df=True,df=daily, outfolder=outfolder,outFile='daily_time.csv')
    daily_bar.cal_threshold("15min_avg")
    threshold = daily_bar.get_threshold()

    generator = bg.bar_generate(inputFile=outfolder+inputfile_min,outFile="dol_bar.csv",outfolder=outfolder)
    generator.set_threshold(threshold)
    generator.convert_dol_bar()
"""
add features to dol bar and store to x_features.csv
clean x_features dataset by droping nans and store to x_features_clean.csv
"""
def add_features(outfolder,inputfile="dol_bar.csv"):
    inputfile = outfolder+inputfile
    pre = preprocess.Preprocess(inputfile)
    print('compute x_features.csv')
    x_features = pre.x_feature2()
    x_features.to_csv(outfolder+"x_features.csv")
    df = pre.clean_df() 
    df.to_csv(outfolder+"x_features_clean.csv")


"""
get label file 
input x_features.csv
"""
def get_labels(outfolder,inputfile="x_features.csv"):
    inputfile = outfolder+inputfile
    pre = preprocess.Preprocess(inputfile) 
    df = pre.label_fix(is_infile=True,inputfile=inputfile)
    print(df.head())
    df.to_csv(outfolder+"labels.csv")
    return df 

def get_labels_no_side(outfolder,inputfile="x_features.csv"):
    inputfile = outfolder+inputfile
    pre = preprocess.Preprocess(inputfile) 
    df = pre.label_fix_no_side(is_infile=True,inputfile=inputfile)
    print(df.head())
    df.to_csv(outfolder+"labels_no_side.csv")
    return df 
"""
generate training dataset x_y.csv

"""
def get_training_dataset(outfolder,x_file="x_features_clean.csv",y_file="labels.csv"):
    x_file = outfolder+x_file
    y_file = outfolder+y_file

    x_data = pd.read_csv(x_file,index_col=0)
    y_data =pd.read_csv(y_file,index_col=0)
    x_data.index = pd.to_datetime(x_data['date_time'])
    x_data.drop(columns=['date_time'],inplace=True)
    y_data.index = pd.to_datetime(y_data.index)
    y_data.loc[(y_data.bin==-1),'bin']=0

    features = ['mom1', 'mom2', 'mom3', 'mom4', 'mom5',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4',
       'autocorr_5', 'log_t1', 'log_t2', 'log_t3', 'log_t4', 'log_t5', 'log_ret','volatility','srsi','fast_mavg','slow_mavg']
    # drop all non-feature columns 
    x_y = x_data[features]
    # add y to x_data
    x_y['y']=y_data.bin
    x_y.dropna(inplace=True)
    x_y.to_csv(outfolder+"x_y.csv")
