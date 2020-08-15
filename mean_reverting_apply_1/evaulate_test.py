from evaulate import evaulate
import pandas as pd 

def evaulate_ex(folder,subfolder):
    subfolder = folder+subfolder

    pre_file = subfolder+"test_predictions.csv"
    label_file = folder+"labels_fix_close.csv"

    ev = evaulate(label_file,pre_file,subfolder)
    ev.long_stats()
    ev.short_stats()

folder = "./BTCUSDT/"
subfolder= ["min-fix5/","min-fix-reg/","min-fix2/","min-fix/","min-fix3/"]
# subfolder= []
# for i in range(1,5):
#     subfolder.append('close-fix'+str(i)+"/")
for i in subfolder:
    evaulate_ex(folder,i)

