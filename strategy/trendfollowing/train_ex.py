import train
import os
import unicodedata
import pandas as pd


def get_datafiles():

    folders = []
    for f in os.listdir("./"):
        if os.path.isdir(f) and f != "training_history":
            folders.append(f)
    datafiles = {}
    for f in folders:
        for i in os.listdir(f):
            if "DS_Store" in i:
                continue
            datafiles[f+"/"+i] = i
    return datafiles


pts = {151: [1.5, 1], 21: [2, 1], 11: [1, 1]}
min_ret = [0.01, 0.02, 0.03, 0.04, 0.05]


def train_ex():
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
            three_model_train(three_folder, pts[p], m)


def three_model_train(output_folder, pts_val, min_ret):
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
        n += 1
        try:
            train_one_model(path, f, "trend_following_weights",
                            pts_val, min_ret)
        except:
            with open("error_training.txt", "a") as myfile:
                myfile.write(path)
                myfile.write(f)
        try:
            train_one_model(path, f, "trend_following", pts_val, min_ret)
        except:
            with open("error_training.txt", "a") as myfile:
                myfile.write(path)
                myfile.write(f)
        try:
            train_one_model(path, f, "mean_reverting", pts_val, min_ret)
        except:
            with open("error_training.txt", "a") as myfile:
                myfile.write(path)
                myfile.write(f)


def train_one_model(path, datafile, model_type, pts_val, min_ret):
    f = path+"_"+model_type
    if not os.path.isdir(f):
        os.mkdir(f)
    t = train.Train(f, datafile)
    if model_type == "trend_following_weights":
        t.training("trend_following_weights")
    elif model_type == "trend_following":
        t.training("trend_following")
    elif model_type == "mean_reverting":
        t.training("mean_reverting")
    else:
        print("error")


train_ex()
