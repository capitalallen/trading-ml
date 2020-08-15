
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import roc_curve
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt
import pandas as pd 
from joblib import dump, load
import json
class Model: 
    """
    constructor:
    - input: dataset
        -> last column is y 
    """
    def __init__(self,df,regu=False):
        self.df = df  
        if regu:
            self.parameters = {'max_depth': [2, 3, 4, 5, 7,10,15,20,25,30,35],
                               'n_estimators': [1, 10, 25, 50, 100, 256, 512,1024,1200],
                               'random_state': [42],
                               'max_features':[10],
                               'max_depth':[10],
                               'min_samples_leaf':[2,3]}
        else:
            self.parameters = {'max_depth': [2, 3, 4, 5, 7,10,15,20,25,30,35],
                               'n_estimators': [1, 10, 25, 50, 100, 256, 512,1024,1200],
                               'random_state': [42]}
    
    """
    split dataset 80:20 
    """
    def split_dataset(self,test_size=0.2):
        self.y = self.df['y']
        self.x = self.df.drop(columns=['y'])
        self.x_train, self.x_validate, self.y_train, self.y_validate = train_test_split(
            self.x, self.y, test_size=test_size, shuffle=False)
        train_df = pd.concat([self.y_train, self.x_train], axis=1, join='inner')
        # print(self.y_train.index)
        # Upsample the training data to have a 50 - 50 split
        # https://elitedatascience.com/imbalanced-classes
        majority = train_df[train_df['y'] == 0]
        minority = train_df[train_df['y'] == 1]

        new_minority = resample(minority,
                                replace=True,     # sample with replacement
                                # to match majority class
                                n_samples=majority.shape[0],
                                random_state=42)
    def get_columns(self):
        return list(self.x_train.columns)
        
    def perform_grid_search(self):
        rf = RandomForestClassifier(criterion='entropy')

        clf = GridSearchCV(rf, self.parameters, cv=4,
                           scoring='roc_auc', n_jobs=3)
        clf.fit(self.x_train, self.y_train)
        # clf.cv_results_['mean_test_score'],
        return (clf.best_params_['n_estimators'], clf.best_params_['max_depth'])
    
    def train(self):
        n_estimator, depth = self.perform_grid_search()
        c_random_state = 42
        self.rf = RandomForestClassifier(max_depth=depth, n_estimators=n_estimator,
                                         criterion='entropy', random_state=c_random_state)
        self.rf.fit(self.x_train, self.y_train.values.ravel())        


    def performance_matrics_accuracy_train(self,outfile='matrics_accuracy_train.png',outfolder=None,reportJson='reports_train.json'):
        if outfolder:
            outfile = outfolder + "/" + outfile 
            reportJson = outfolder + '/' + reportJson
        y_pred_rf = self.rf.predict_proba(self.x_train)[:, 1]
        self.y_pred_train = self.rf.predict(self.x_train)
        fpr_rf, tpr_rf, _ = roc_curve(self.y_pred_train, y_pred_rf)

        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr_rf, tpr_rf, label='RF')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.savefig(outfile)        
        classification = classification_report(self.y_train, self.y_pred_train,output_dict=True)
        matrix = confusion_matrix(self.y_train, self.y_pred_train)
        accuracy = accuracy_score(self.y_train, self.y_pred_train)
        with open(reportJson, 'w') as outfile:
            json.dump(classification, outfile)
            json.dump({"confusion_matrix":[matrix.tolist()],"accuracy_score":accuracy},outfile)
    def performance_matrics_accuracy(self,outfile='matrics_accuracy_validate.png',outfolder=None,reportJson='reports_test.json'):
        if outfolder:
            outfile = outfolder + "/" + outfile 
            reportJson = outfolder +'/' + reportJson
        y_pred_rf = self.rf.predict_proba(self.x_validate)[:, 1]
        self.y_pred = self.rf.predict(self.x_validate)
        self.test_prediction = pd.Series(data=self.y_pred,index=self.y_validate.index)
        fpr_rf, tpr_rf, _ = roc_curve(self.y_validate, y_pred_rf)

        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr_rf, tpr_rf, label='RF')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.savefig(outfile)        
        classification = classification_report(self.y_validate, self.y_pred,output_dict=True)
        matrix = confusion_matrix(self.y_validate, self.y_pred)
        accuracy = accuracy_score(self.y_validate, self.y_pred)

        with open(reportJson, 'w') as f:
            json.dump(classification, f)
            json.dump({"confusion_matrix":[matrix.tolist()],"accuracy_score":accuracy},f)

    def feature_importance(self, outfile="feature_importance.png",outfolder=None):

        if outfolder:
            outfile = outfolder + "/" + outfile
        # Feature Importance
        title = 'Feature Importance:'
        figsize = (15, 5)

        feat_imp = pd.DataFrame({'Importance': self.rf.feature_importances_})
        feat_imp['feature'] = self.x.columns
        feat_imp.sort_values(by='Importance', ascending=False, inplace=True)
        feat_imp = feat_imp

        feat_imp.sort_values(by='Importance', inplace=True)
        feat_imp = feat_imp.set_index('feature', drop=True)
        feat_imp.plot.barh(title=title, figsize=figsize)
        plt.xlabel('Feature Importance Score')
        plt.savefig(outfile)
    
    # gt predictions 
    def get_prediction(self):
        return self.test_prediction
    # store test predictions 
    def store_prediction(self,outfile='test_predictions.csv',outfolder=None):
        if outfolder:
            outfile = outfolder + "/" + outfile 
        self.test_prediction.to_frame().to_csv(outfile)

    def save_model(self,outfile='model.joblib',outfolder=None):
        if outfolder:
            outfile = outfolder + "/" + outfile 
        dump(self.rf,outfile)        