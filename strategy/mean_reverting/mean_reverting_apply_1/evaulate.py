import pandas as pd 
import matplotlib.pyplot as plt 
import json 
class evaulate:
    def __init__(self,label_file,prediction_file,output_folder):
        self.labels = pd.read_csv(label_file,index_col=0)
        self.labels.index = pd.to_datetime(self.labels.index)
        self.predictions = pd.read_csv(prediction_file,index_col=0)
        self.predictions.index = pd.to_datetime(self.predictions.index)
        self.out_folder=output_folder
        self.jsonfile = self.out_folder+'backtesting.json'
    def cum_return(self,df):
        tmp_df = df.copy()
        cul = 0
        for index,row in tmp_df.iterrows():
            cul += row['ret']
            tmp_df.set_value(index,'ret',cul)
        return tmp_df
    def long_stats(self):
        results = {}
        long_pre = self.predictions[self.predictions['0']==1]
        long_labels=self.labels.loc[long_pre.index]

        side0 = long_labels[long_labels.side==-1]
        side1 = long_labels[long_labels.side==1]
        # side1.to_csv(self.out_folder+"side1_origin.csv")

        try:
            #positive rate
            results['pred==1,ret>0 %']=long_labels[long_labels.ret>0].shape[0]/long_labels.shape[0]
            results['pred==1 and side=-1,ret>0 %']=side0[side0.ret>0].shape[0]/side0.shape[0]
            results['pred==1 and side==1, ret>0 %']=side1[side1.ret>0].shape[0]/side1.shape[0]
        except:
            print("positive rate")
        plt.scatter(long_labels.index,long_labels.ret,label="pred=1")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred1.png")
        plt.close()
        
        plt.plot(side0.index,side0.ret,label="pred=1 and side=-1")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred1_side-1.png")
        plt.close()
        
        plt.plot(side1.index,side1.ret,label="pred=1 and side=-1")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred1_side1.png")
        plt.close()

        #plot cum return
        tmp1=self.cum_return(long_labels)
        tmp2=self.cum_return(side0)
        tmp3=self.cum_return(side1) 
        plt.plot(tmp1.index,tmp1.ret,label='pred1')
        plt.plot(tmp2.index,tmp2.ret,label='pred=1 & side=-1')
        plt.plot(tmp3.index,tmp3.ret,label='pred=1 & side=1')
        plt.legend()
        plt.savefig(self.out_folder+"pred1_cum_return.png")
        plt.close()

        #plot cum return
        # long_labels.to_csv(self.out_folder+"back.csv")
        long_labels.loc[(long_labels.ret<-0.02),"ret"]=-0.02
        # long_labels.to_csv(self.out_folder+"back1.csv")
        side0.loc[(side0.ret<-0.02),"ret"]=-0.02
        side1.loc[(side1.ret<-0.02),"ret"]=-0.02  
        tmp1=self.cum_return(long_labels)
        tmp2=self.cum_return(side0)
        tmp3=self.cum_return(side1)
        
        # side1.to_csv(self.out_folder+"side1.csv")
        # tmp3.to_csv(self.out_folder+"tmp3.csv")

        plt.plot(tmp1.index,tmp1.ret,label='pred1')
        plt.plot(tmp2.index,tmp2.ret,label='pred=1 & side=-1')
        plt.plot(tmp3.index,tmp3.ret,label='pred=1 & side=1')
        plt.legend()    
        plt.savefig(self.out_folder+"pred1_cum_return_stop_limit.png")
        plt.close()
        with open(self.jsonfile,'w') as f:
            json.dump(results,f)
    def short_stats(self):
        results = {}
        short_pre = self.predictions[self.predictions['0']==0]
        short_labels=self.labels.loc[short_pre.index]

        side0 = short_labels[short_labels.side==-1]
        side1 = short_labels[short_labels.side==1]

        try:
            #positive rate
            results['pred==0,ret<0 %']=short_labels[short_labels.ret<0].shape[0]/short_labels.shape[0]
            results['pred==0 and side=-1,ret<0 %']=side0[side0.ret<0].shape[0]/side0.shape[0]
            results['pred==0 and side==1, ret<0 %']=side1[side1.ret<0].shape[0]/side1.shape[0]
        except:
            print("positive rate")
        plt.scatter(short_labels.index,short_labels.ret,label="pred=0")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred0.png")
        plt.close()

        plt.plot(side0.index,side0.ret,label="pred=0 and side=-1")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred0_side-1.png")
        plt.close()

        plt.plot(side1.index,side1.ret,label="pred=0 and side=-1")
        plt.legend()
        plt.savefig(self.out_folder+"returns_pred0_side1.png")
        plt.close()
        #plot cum return
        tmp1=self.cum_return(short_labels)
        tmp2=self.cum_return(side0)
        tmp3=self.cum_return(side1) 
        plt.plot(tmp1.index,tmp1.ret,label='pred0')
        plt.plot(tmp2.index,tmp2.ret,label='pred=0 & side=-1')
        plt.plot(tmp3.index,tmp3.ret,label='pred=0 & side=1')
        plt.legend()
        plt.savefig(self.out_folder+"pred0_cum_return.png")
        plt.close()
        #plot cum return
        short_labels.loc[(short_labels.ret>0.02),'ret']=0.02
        side0.loc[(side0.ret>0.02),'ret']=0.02
        side1.loc[(side1.ret>0.02),'ret']=0.02        
        tmp1=self.cum_return(short_labels)
        tmp2=self.cum_return(side0)
        tmp3=self.cum_return(side1) 
        plt.plot(tmp1.index,tmp1.ret,label='pred0')
        plt.plot(tmp2.index,tmp2.ret,label='pred=0 & side=-1')
        plt.plot(tmp3.index,tmp3.ret,label='pred=0 & side=1')
        plt.legend()
        plt.savefig(self.out_folder+"pred0_cum_return_stop_limit.png")
        plt.close()
        with open(self.jsonfile,'a') as f:
            json.dump(results,f)