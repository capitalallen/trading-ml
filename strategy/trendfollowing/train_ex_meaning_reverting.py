import train
import os
import unicodedata
import pandas as pd
import store_results

def get_datafiles():

    folders = "./new_training_set"
    datafiles = {}
    for i in os.listdir(folders):
        if "DS_Store" in i:
            continue
        datafiles[folders+"/"+i] = i
    return datafiles


pts = {2:[0,2],12:[1,2],21: [2, 1]}
min_ret = [0.01,0.03,0.05,0.1]
num_days = [1,2,4]

def train_ex_mean_reverting():
    one_folder = "./training_history/"
    for p in pts:
        two_folder = one_folder+str(p)
        if not os.path.isdir(two_folder):
            os.mkdir(two_folder)
        for m in min_ret:
            three_folder = two_folder+"/"+str(m)
            if not os.path.isdir(three_folder):
                os.mkdir(three_folder)
            three_folder += "/"
            for n in num_days:
                four_folder = three_folder+str(n)+"/"
                if not os.path.isdir(four_folder):
                    os.mkdir(four_folder)
                three_model_train(four_folder, pts[p], m,n)


def three_model_train(output_folder, pts_val, min_ret,num_days):
    """
    test
    """
    # define 2 data folders
    # store filename from 2 data folders to a list
    datafiles = get_datafiles()
    n = 0
    for f in datafiles:
        # print(output_folder, datafiles[f][:11], str(n))
        path = output_folder+datafiles[f][:11]+str(n)
        #path = output_folder+datafiles[:11]+str(n)
        try:
            train_one_model(path, f, "mean_reverting",
                            pts_val, min_ret,num_days)
        except:
            d = {"path":path,"pts_val":pts_val,"min_ret":min_ret,"num_days":num_days}
            s = store_results.Store_model_result()
            s.record_error(d)
            print("error recorded")
        train_one_model(path, f, "mean_reverting",pts_val, min_ret,num_days)
        # try:
        #     train_one_model(path, f, "trend_following", pts_val, min_ret)
        # except:
        #     with open("error_training.txt", "a") as myfile:
        #         myfile.write(path)
        #         myfile.write(f)
        # try:
        #     train_one_model(path, f, "mean_reverting", pts_val, min_ret)
        # except:
        #     with open("error_training.txt", "a") as myfile:
        #         myfile.write(path)
        #         myfile.write(f)


def train_one_model(path, datafile, model_type, pts_val, min_ret,num_days):
    path += "/"
    if not os.path.isdir(path):
        os.mkdir(path)
    t = train.Train(path, datafile)
    if model_type == "trend_following_weights":
        t.training("trend_following_weights")
    elif model_type == "trend_following":
        t.training("trend_following")
    elif model_type == "mean_reverting":
        t.training("mean_reverting",pts_val, min_ret,num_days)
    else:
        print("error")


train_ex_mean_reverting()
