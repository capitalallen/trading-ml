import train_trend_following


def test(folder="./test_set"):
    t = train_trend_following.Train_trend_following()
    t.get_datafiles(folder)
    t.perform_training([1, 2], 0.02, 2)


def perform_training(folder="./new_training_set/"):
    t = train_trend_following.Train_trend_following()
    t.get_datafiles(folder)
    pts = [[1.5, 1], [2, 1], [1, 1]]
    ret = [0.02, 0.04, 0.06]
    num_days = [2, 3, 4]
    for p in pts:
        for r in ret:
            for n in num_days:
                t.perform_training(p, r, n)


test()
# perform_training()
