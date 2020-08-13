# from ... import bar_generator
import sys
sys.path.append("../bar_generator")
sys.path.append("../data_downloader")
sys.path.append("../labeling")
import data_getter 
import filter_label
import bar_generate
import os 
# from ...bar_generator import bar_generate
"""
dataset_getter()
input: pair_name, start_time, output_folder
1, call data_downloader 
    -> daily data 
    -> 5min data 
    -> store to output_folder 
2, call bar_generator 
    -> cal threshold daily_average/50
    -> dollar bar 
    -> store bars to output_folder 
3, call labelling
    ->filter
    ->label 
"""


def store_raw_data(pair, start_time, output_folder,out_bar_filename,min_kline_size='5m'):
    if not start_time:
        start_time = "01 Nov 2017"
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    download = data_getter.data_getter()
    daily_df_file = download.get_all_binance(pair,kline_size="1d",start_time=start_time,folder=output_folder,save=False)
    daily_df_file = daily_df_file.astype(float)
    daily_df_file.to_csv(output_folder+"/"+"daily_timebar.csv")
    min_df_file = download.get_all_binance(pair,kline_size="5m",start_time=start_time,save=False)
    min_df_file = min_df_file.astype(float)
    min_df_file.to_csv(output_folder+"/"+"minute_timebar.csv")

    # get threshold
    daily = bar_generate.bar_generate(read_df=True,df=daily_df_file, outfolder=output_folder,outFile='daily_time.csv')
    daily.cal_threshold("daily_av_50")
    threshold = daily.get_threshold()

    #convert bars 
    generator = bar_generate.bar_generate(read_df=True,df=min_df_file,outFile=out_bar_filename,outfolder=output_folder)
    generator.set_threshold(threshold)
    generator.convert_dol_bar()

def test():
    print('successful')
# store_raw_data("BTCUSDT","01 Nov 2017",'./test',"./test/dol_bar.csv")
