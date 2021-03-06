# -*- coding: utf-8 -*-
"""code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1diw7ruEqc0P7WQyxbA-2GS7wqfi5HyBt
"""

from math import sqrt
import numpy as np
import sklearn
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import matplotlib.pyplot as plt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from pandas import read_csv
from datetime import datetime
from keras.layers import Bidirectional
import datetime
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from numpy import array
import time

def rmse(pred, actual):
    error = np.subtract(pred, actual)
    sqerror= np.sum(np.square(error))/actual.shape[0]
    return np.sqrt(sqerror)

def MODEL_LSTM(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden):
    n_features = 1
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], n_features))
    print(x_train.shape)
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], n_features))
    print(x_test.shape)
    
    train_acc=np.zeros(Num_Exp)
    test_acc=np.zeros(Num_Exp)
    Step_RMSE=np.zeros([Num_Exp,n_steps_out])
    
    model = Sequential()
    model.add(LSTM(Hidden, activation='relu', input_shape=(n_steps_in,n_features)))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    Best_RMSE=1000   #Assigning a large number 
    
    start_time=time.time()
    for run in range(Num_Exp):
        print("Experiment",run+1,"in progress")
        # fit model
        model.fit(x_train, y_train, epochs=Epochs,batch_size=64, verbose=0, shuffle=False)
        y_predicttrain = model.predict(x_train)
        y_predicttest = model.predict(x_test)
        train_acc[run] = rmse( y_predicttrain,y_train) 
        test_acc[run] = rmse( y_predicttest, y_test) 
        if test_acc[run]<Best_RMSE:
            Best_RMSE=test_acc[run]
            Best_Predict_Test=y_predicttest
        for j in range(n_steps_out):
            Step_RMSE[run][j]=rmse(y_predicttest[:,j], y_test[:,j])
            
    print("Total time for",Num_Exp,"experiments",time.time()-start_time)
    return train_acc,test_acc,Step_RMSE,Best_Predict_Test


def MODEL_Bi_LSTM(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden):
    n_features = 1
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], n_features))
    print(x_train.shape)
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], n_features))
    print(x_test.shape)
    
    train_acc=np.zeros(Num_Exp)
    test_acc=np.zeros(Num_Exp)
    Step_RMSE=np.zeros([Num_Exp,n_steps_out])
    
    model = Sequential()
    model.add(Bidirectional(LSTM(Hidden, activation='relu'), input_shape=(n_steps_in,n_features)))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    
    Best_RMSE=1000   #Assigning a large number 
    start_time=time.time()
    for run in range(Num_Exp):
        print("Experiment",run+1,"in progress")
        # fit model
        model.fit(x_train, y_train, epochs=Epochs,batch_size=64, verbose=0, shuffle=False)
        y_predicttrain = model.predict(x_train)
        y_predicttest = model.predict(x_test)
        train_acc[run] = rmse( y_predicttrain,y_train) 
        test_acc[run] = rmse( y_predicttest, y_test) 
        if test_acc[run]<Best_RMSE:
            Best_RMSE=test_acc[run]
            Best_Predict_Test=y_predicttest
        for j in range(n_steps_out):
            Step_RMSE[run][j]=rmse(y_predicttest[:,j], y_test[:,j])
            
    print("Total time for",Num_Exp,"experiments",time.time()-start_time)
    return train_acc,test_acc,Step_RMSE,Best_Predict_Test


def MODEL_EN_DC(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden):
    n_features = 1
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], n_features))
    print(x_train.shape)
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], n_features))
    print(x_test.shape)
    y_train = y_train.reshape((y_train.shape[0], y_train.shape[1], n_features))
    print(y_train.shape)
    y_test = y_test.reshape((y_test.shape[0], y_test.shape[1], n_features))
    print(y_test.shape)
    
    train_acc=np.zeros(Num_Exp)
    test_acc=np.zeros(Num_Exp)
    Step_RMSE=np.zeros([Num_Exp,n_steps_out])
    
    model = Sequential()
    model.add(LSTM(Hidden, activation='relu',input_shape=(n_steps_in,n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(Hidden, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(1,activation='relu')))
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    
    Best_RMSE=1000   #Assigning a large number 
    start_time=time.time()
    for run in range(Num_Exp):
        print("Experiment",run+1,"in progress")
        # fit model
        model.fit(x_train, y_train, epochs=Epochs,batch_size=64, verbose=0, shuffle=False)
        y_predicttrain = model.predict(x_train)
        y_predicttest = model.predict(x_test)
        train_acc[run] = rmse( y_predicttrain,y_train) 
        test_acc[run] = rmse( y_predicttest, y_test) 
        if test_acc[run]<Best_RMSE:
            Best_RMSE=test_acc[run]
            Best_Predict_Test=y_predicttest
        for j in range(n_steps_out):
            Step_RMSE[run][j]=rmse(y_predicttest[:,j,0], y_test[:,j,0])
            
    print("Total time for",Num_Exp,"experiments",time.time()-start_time)
    return train_acc,test_acc,Step_RMSE,Best_Predict_Test.reshape(y_test.shape[0], y_test.shape[1])

def Plot_Mean(name,TrainRMSE_mean,TestRMSE_mean):
    labels = ['TrainRMSE','TestRMSE']
    LSTM=[TrainRMSE_mean[0],TestRMSE_mean[0]]
    Bi_LSTM=[TrainRMSE_mean[1],TestRMSE_mean[1]]
    EN_DC=[TrainRMSE_mean[2],TestRMSE_mean[2]]
    width = 0.1  # the width of the bars
    Plot(name,labels,width,LSTM,Bi_LSTM,EN_DC,"Mean","Train&Test_RMSE_Mean_Comparison")


def Plot_Std(name,TrainRMSE_Std,TestRMSE_Std):
    labels = ['TrainRMSE','TestRMSE']
    LSTM=[TrainRMSE_Std[0],TestRMSE_Std[0]]
    Bi_LSTM=[TrainRMSE_Std[1],TestRMSE_Std[1]]
    EN_DC=[TrainRMSE_Std[2],TestRMSE_Std[2]]
    width = 0.1  # the width of the bars
    Plot(name,labels,width,LSTM,Bi_LSTM,EN_DC,"Standard Deviation","Train&Test_RMSE_Std_Comparison")

def Plot_Step_RMSE_Mean(name,Step_RMSE_mean):
    LSTM=Step_RMSE_mean[0,:]
    Bi_LSTM=Step_RMSE_mean[1,:]
    EN_DC=Step_RMSE_mean[2,:]
    labels = []
    for j in range(Step_RMSE_mean.shape[1]):
        labels=np.concatenate((labels,[str(j+1)]))
    width = 0.1  # the width of the bars
    Plot(name,labels,width,LSTM,Bi_LSTM,EN_DC,"RMSE_Mean","Step_RMSE_Comparison")
    

def Plot(name,labels,width,LSTM,Bi_LSTM,EN_DC,typ,Gname):
    r1 = np.arange(len(labels))
    r2 = [x + width for x in r1]
    r3 = [x + width for x in r2]

    fig, ax = plt.subplots()
    rects1 = ax.bar(r1, LSTM, width, label='LSTM')
    rects2 = ax.bar(r2, Bi_LSTM, width, label='Bi_LSTM')
    rects3 = ax.bar(r3, EN_DC, width, label='EN_DC')

    plt.ylabel(typ)
    ax.set_title('Stacked LSTM vs Bi-LSTM vs EN-DC LSTM')
    plt.xticks([r + width for r in range(len(LSTM))], labels)
    ax.legend()
    fig.tight_layout()
    plt.savefig("/content/drive/My Drive/covid project/Model/Results/"+name+"/"+Gname+".png",dpi=100)
    plt.show()

from google.colab import drive
drive.mount('/content/drive')

def main():
    
    n_steps_in, n_steps_out = 5,5
    
    Overall_Analysis=np.zeros([3,10+n_steps_out*5])
    for i in range(1,2):
        problem=i
        if problem ==1:
            
            TrainData = pd.read_csv('/content/drive/My Drive/covid project/Data/Processed_Data/train.csv',index_col = 0)
            TrainData = TrainData.values
            TestData = pd.read_csv('/content/drive/My Drive/covid project/Data/Processed_Data/test.csv',index_col = 0)
            TestData = TestData.values
            name= "ALL_INDIA" 

        x_train = TrainData[:,0:n_steps_in]
        y_train = TrainData[:,n_steps_in : n_steps_in+n_steps_out ]
        x_test = TestData[:,0:n_steps_in]
        y_test = TestData[:,n_steps_in : n_steps_in+n_steps_out]

        print(name)
        Num_Exp=30    #No. of experiments
        Epochs=300
        Hidden=20
        TrainRMSE_mean=np.zeros(4)
        TestRMSE_mean=np.zeros(4)
        TrainRMSE_Std=np.zeros(4)
        TestRMSE_Std=np.zeros(4)
        Step_RMSE_mean=np.zeros([4,n_steps_out])
        train_acc=np.zeros(Num_Exp)
        test_acc=np.zeros(Num_Exp)
        Step_RMSE=np.zeros([Num_Exp,n_steps_out])


        for k in range(1,4):

            method=k
            if method ==1:
                train_acc,test_acc,Step_RMSE,Best_Predict_Test=MODEL_LSTM(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden)
                Mname="MODEL_LSTM"
            if method ==2:
                train_acc,test_acc,Step_RMSE,Best_Predict_Test=MODEL_Bi_LSTM(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden)
                Mname="MODEL_Bi_LSTM"
            if method ==3:
                train_acc,test_acc,Step_RMSE,Best_Predict_Test=MODEL_EN_DC(x_train,x_test,y_train,y_test,Num_Exp,n_steps_in,n_steps_out,Epochs,Hidden)
                Mname="MODEL_EN_DC"
                

            print(Mname)

            arr = np.dstack((train_acc,test_acc))
            arr=arr.reshape(Num_Exp,2)
            arr=np.concatenate((arr,Step_RMSE), axis=1)
            arr=arr.reshape(Num_Exp,2+n_steps_out)
            
            ExpIndex=np.array([])
            for j in range(Num_Exp):
                ExpIndex=np.concatenate((ExpIndex,["Exp"+str(j+1)]))

            TrainRMSE_mean[k-1]=np.mean(train_acc)
            TestRMSE_mean[k-1]=np.mean(test_acc)
            TrainRMSE_Std[k-1]=np.std(train_acc)
            TestRMSE_Std[k-1]=np.std(test_acc)
            ExpIndex1=['TrainRMSE','TestRMSE']
            for j in range(n_steps_out):
              Step_RMSE_mean[k-1][j]=np.mean(Step_RMSE[:,j])
              ExpIndex1=np.concatenate((ExpIndex1,["Step"+str(j+1)]))
                
            arr=np.round_(arr, decimals = 5) 
            arr = pd.DataFrame(arr, index = ExpIndex , columns = ExpIndex1)
            arr.to_csv("/content/drive/My Drive/covid project/Model/Results/"+name+"/"+Mname+"/ExpAnalysis.csv")
            print(arr)
            
            Train_Mean=np.mean(train_acc)
            Train_Std=np.std(train_acc)
            Train_CI_LB= Train_Mean-1.96*(Train_Std/np.sqrt(Num_Exp))
            Train_CI_UB= Train_Mean+1.96*(Train_Std/np.sqrt(Num_Exp))
            
            Test_Mean=np.mean(test_acc)
            Test_Std=np.std(test_acc)
            Test_CI_LB= Test_Mean-1.96*(Test_Std/np.sqrt(Num_Exp))
            Test_CI_UB= Test_Mean+1.96*(Test_Std/np.sqrt(Num_Exp))
            
            Overall_Analysis[(i-1)*1+(k-1)][0]=Train_Mean
            Overall_Analysis[(i-1)*1+(k-1)][1]=Train_Std
            Overall_Analysis[(i-1)*1+(k-1)][2]=Train_CI_LB
            Overall_Analysis[(i-1)*1+(k-1)][3]=Train_CI_UB
            Overall_Analysis[(i-1)*1+(k-1)][4]=np.min(train_acc)
            Overall_Analysis[(i-1)*1+(k-1)][5]=Test_Mean
            Overall_Analysis[(i-1)*1+(k-1)][6]=Test_Std
            Overall_Analysis[(i-1)*1+(k-1)][7]=Test_CI_LB
            Overall_Analysis[(i-1)*1+(k-1)][8]=Test_CI_UB
            Overall_Analysis[(i-1)*1+(k-1)][9]=np.min(test_acc)
            
            arr1 = np.vstack(([Train_Mean,Train_Std,Train_CI_LB,Train_CI_UB,np.min(train_acc),np.max(train_acc)],[Test_Mean,Test_Std,Test_CI_LB,Test_CI_UB,np.min(test_acc),np.max(test_acc)]))
            
            for j in range(n_steps_out):
                Step_mean = np.mean(Step_RMSE[:,j])
                Step_std = np.std(Step_RMSE[:,j])
                Step_min = np.min(Step_RMSE[:,j])
                Step_CI_LB= Step_mean-1.96*(Step_std/np.sqrt(Num_Exp))
                Step_CI_UB= Step_mean+1.96*(Step_std/np.sqrt(Num_Exp))
                arr1=np.vstack((arr1,[Step_mean,Step_std,Step_CI_LB,Step_CI_UB,Step_min,np.max(Step_RMSE[:,j])]))
                Overall_Analysis[(i-1)*7+(k-1)][5*j+10]= Step_mean
                Overall_Analysis[(i-1)*7+(k-1)][5*j+11]= Step_std
                Overall_Analysis[(i-1)*7+(k-1)][5*j+12]= Step_CI_LB
                Overall_Analysis[(i-1)*7+(k-1)][5*j+13]= Step_CI_UB
                Overall_Analysis[(i-1)*7+(k-1)][5*j+14]= Step_min
            arr1=np.round_(arr1, decimals = 5) 
            arr1 = pd.DataFrame(arr1, index=ExpIndex1, columns = ['Mean','Standard Deviation','CI_LB','CI_UB','Min','Max'])
            print(arr1)
            arr1.to_csv("/content/drive/My Drive/covid project/Model/Results/"+name+"/"+Mname+"/OverallAnalysis.csv")
            
            x_data=np.linspace(0,y_test.shape[0], num=y_test.shape[0])
            for j in range(n_steps_out):
                plt.figure()
                plt.plot(x_data, y_test[:,j], label='actual')
                plt.plot(x_data, Best_Predict_Test[:,j], label='predicted')
                plt.ylabel('RMSE')  
                plt.xlabel('Time (samples)') 
                plt.title('Actual vs Predicted')
                plt.legend()
                plt.savefig("/content/drive/My Drive/covid project/Model/Results/"+name+"/"+Mname+'/pred_Step'+str(j+1)+'.png',dpi=300) 
                plt.show()
                plt.close()
        #Plot mean of train_RMSE and test_RMSE
        Plot_Mean(name,TrainRMSE_mean,TestRMSE_mean)
        #Plot Std of train_RMSE and test_RMSE
        Plot_Std(name,TrainRMSE_Std,TestRMSE_Std)
        #Plot Step wise RMSE mean for different methods
        Plot_Step_RMSE_Mean(name,Step_RMSE_mean)
if __name__ == "__main__": main()

