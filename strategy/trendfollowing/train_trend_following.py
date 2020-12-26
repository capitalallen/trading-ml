import train
import os
import unicodedata
import pandas as pd
import store_results


class Train_trend_following:
    def __init__(self):
        self.datafiles = {}
    # get all datafiles

    def get_datafiles(self, folder="./new_training_set"):
        for i in os.listdir(folder):
            if "DS_Store" in i:
                continue
            self.datafiles[folder+"/"+i] = i

    def perform_training(self, pts, ret, num_day):
        path = "./training_history/" + \
            str(pts) + "_"+str(ret)+"_"+str(num_day)+"/"
        if not os.path.isdir(path):
            os.mkdir(path)
        if not self.datafiles:
            print("datafiles empty")
            return
        for i in self.datafiles:
            folder = path+self.datafiles[i][:11]+"/"
            if not os.path.isdir(folder):
                os.mkdir(folder)
            try:
                t = train.Train(folder, i)
                t.training("trend_following_weights",
                           pts, ret, num_day)
            except:
                d = {"path": path, "pts_val": pts,
                     "min_ret": ret, "num_days": num_day}
                s = store_results.Store_model_result()
                s.record_error(d)
                print("error recorded")
