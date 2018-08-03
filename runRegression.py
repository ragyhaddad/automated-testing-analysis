#!/bin/bash/Python
import pandas as pd
import numpy as np 
import seaborn as sns; sns.set()
from sklearn import linear_model
import sys
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# Global Variables
df = 0
fig, axs = plt.subplots(2,2, figsize=(30, 20), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace =0.5, wspace=0.5)
axs = axs.ravel()
regr = 0
X = 0
Y = 0
X_train = 0
Y_train = 0
X_test = 0
Y_test = 0
Y_predict = 0  
file_array = []
columns = 4
rows = 5

#PDF to save data
pp = PdfPages('regression.pdf')
#Reads file and creates a dataframe
def readFile(file_path):
    global df
    df = pd.read_csv(file_path,skiprows=[1])
    df = df.dropna()
    #Remove last line 
    df = df.drop(df.index[len(df)-1])
    print(df.shape)

#Split function
def split(x_col, y_col, percent_train=100, percent_test=100):
    global X , Y, X_train, Y_train, X_test, Y_test, df
    X = df.iloc[:,x_col].values.reshape(-1,1)
    Y = df.iloc[:,y_col].values.reshape(-1,1)
    split_percent = int((float(percent_train)/100) * len(X)) -1
    test_percent = int((float(percent_test)/100) * len(Y)) -1
    print(test_percent)
    print("train ",split_percent)
    print("test ",test_percent)
    X_train = X[:-split_percent]
    X_test = X[-test_percent:]
    Y_train = Y[:-split_percent]
    Y_test = Y[-test_percent:]
    print(df.columns[x_col])
    print(df.columns[y_col])

# Fit Regression Model
def runModel():
    global Y_predict, regr
    regr = linear_model.LinearRegression()
    regr.fit(X_train,Y_train)
    Y_predict = regr.predict(X_test)
    # residuals = Y - Y_predict
    print(Y_predict)
    print('Coefficients:', regr.coef_[0])
    print('Y intercept' , regr.intercept_)
    r_score = r2_score(Y_test, Y_predict)
    print('Variance score:' , r_score)

# Plot Regression Line   
def plotModel():
    plt.subplot(111)
    plt.scatter(X_test, Y_test,  color='blue',alpha=0.5)
    plt.plot(X_test, Y_predict, color='black', linewidth=3)
    # plt.show()

def plotMultiple(x,filename):
    title = 'Bivariate fit ' + df.columns[0] +  ' and ' + df.columns[9]
    fig.suptitle(title)
    sub_title = os.path.basename(filename) + ' Beta: ' + str(regr.coef_[0][0])
    axs[x].set_title(sub_title)
    axs[x].scatter(X_test, Y_test,  color='blue',alpha=0.5)
    axs[x].plot(X_test, Y_predict, color='black', linewidth=3)
    

# Reads a directory and populates an array of file names
def readDirectory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(os.path.join(directory, filename))
            file_path = os.path.join(directory,filename)
            file_array.append(file_path)
    return file_path
		


columns = 2
rows = 2
count = 0
readDirectory(sys.argv[1])
for x in range(24):
    readFile(file_array[x])
    split(0,9,20,80)
    runModel()
    plotMultiple(count,file_array[x])
    count = count + 1
    if(count == 4):
        fig.savefig(pp,format='pdf')
        fig, axs = plt.subplots(2,2, figsize=(30, 20), facecolor='w', edgecolor='k')
        fig.subplots_adjust(hspace =0.5, wspace=0.5)
        axs = axs.ravel()
        count = 0
pp.close()


