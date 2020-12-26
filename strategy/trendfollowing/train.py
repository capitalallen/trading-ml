
import trend_following_weights
import mean_reverting
import trend_following
from sklearn import datasets
from joblib import dump, load
import pandas as pd
from datetime import datetime
import store_results


class Train:
    def __init__(self, folder, datafile):
        self.folder = folder
        self.datafile = datafile
        self.store_model = store_results.Store_model_result()

    def set_folder(self, folder):
        self.folder = folder

    def training(self, model, pt_sl=[0, 2], min_ret=0.0005, num_days=1):
        all_results = {}
        if model == "trend_following_weights":
            # add model type, time and folder
            all_results["model"] = "trend_follwoing_weights"
            all_results["time"] = str(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            all_results["folder"] = self.folder
            all_results["dataset"] = self.datafile
            self.outfile = self.folder+"/trend_follwoing_weights"

            # train the model
            t = trend_following_weights.Trend_following_weights(self.datafile)
            t.process_data(pt_sl, min_ret, num_days)
            t.features()
            t.training_dataset(self.outfile+"features.csv")
            # t.sample_weights()
            # t.perform_grid_search_sample_weights()

            # performance_metrics_meta()
            t.sample_weights()
            t.perform_grid_search_sample_weights()
            # t.feature_importance(self.outfile+"feature_importance.png")

            matrics = t.performance_metrics_meta()
            all_results["performance_metrics_meta"] = {
                "accuracy_score": matrics[1], "classification_report": matrics[2]}

            # save dailty return
            daily_returns = t.validation_metrics()
            daily_returns.to_csv(self.outfile+"_daily_meta_return.csv")

            matrics = t.test_out_of_sampe(self.outfile+"_test_out_of_sampe_performance.png",
                                          kpiImagePath=self.outfile+"test_out_of_kpi.png")
            all_results["performance_test_out_of_sampe"] = {
                "accuracy_score": matrics[1], "classification_report": matrics[2]}
            matrics[3].to_csv(self.outfile+"backtesting_result.csv")

            # save model
            t.save_model(self.outfile+"_model")
            # save result to mongodb
            self.store_model.record_model_trend_following(all_results)
        elif model == "mean_reverting":
            # add model type, time and folder
            all_results["model"] = "mean_reverting"
            all_results["time"] = str(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            all_results["folder"] = self.folder
            all_results["dataset"] = self.datafile

            self.outfile = self.folder+"/mean_reverting"
            m = mean_reverting.Mean_reverting(self.datafile)
            m.add_bbands()
            m.add_rsi()
            m.compute_side()
            m.cusum_filter()
            m.triple_barrier(pt_sl=pt_sl, min_ret=min_ret, num_days=num_days)
            m.features()
            m.split_dataset()
            m.train()
            print(self.outfile)
            matrics = m.performance_matrics_accuracy(
                self.outfile+"_accuracy.png")
            all_results["performance_metrics_meta"] = {
                "accuracy_score": matrics[2], "classification_report": matrics[0]}
            print(all_results)
            m.feature_importance(self.outfile+"_feature_importance.png")
            m.performance_in_sample(self.outfile+"_performance_in_sample.png")

            matrics = m.performance_out_sample(
                self.outfile+"_performance_out_sample.png")
            all_results["performance_test_out_of_sampe"] = {
                "accuracy_score": matrics[2], "classification_report": matrics[0]}
            m.return_history_csv(self.outfile+"_return_history.csv")
            matrics[3].to_csv(self.outfile+"backtesting.csv")
            m.save_model(self.outfile+"model")
            self.store_model.record_model_mean_reverting(all_results)

        elif model == "trend_following":
            self.outfile = self.folder+"/trend_following"

            all_results["model"] = "trend_follwoing"
            all_results["time"] = str(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            all_results["folder"] = self.folder
            all_results["dataset"] = self.datafile

            m = trend_following.Trend_following(self.datafile)
            m.process_data()
            m.features()
            m.training_dataset(self.outfile)
            m.training()

            matrics = m.performance_metrics_meta()
            all_results["performance_metrics_meta"] = {
                "accuracy_score": matrics[1], "classification_report": matrics[2]}
            m.feature_importance_image(self.outfile+"_feature_importance.png")

            matrics = m.validation_metrics(
                self.outfile+"_validation_metrics.png", outfile2=self.outfile+"_daily_return.csv")

            matrics = m.test_out_of_sampe(
                self.outfile+"outputImagePath.png", self.outfile+"kpiImagePath.png")

            m.return_history_csv(self.outfile+"_return_history.csv")

            all_results["performance_test_out_of_sampe"] = {
                "accuracy_score": matrics[1], "classification_report": matrics[2]}
            #all_results["perf_stats_df"] = matrics[3].to_dict(orient='records')
            matrics[3].to_csv(self.outfile+"_backtesting_result_no_fee.csv")
            self.store_model.record_model(all_results)
        else:
            print("model not defined")
