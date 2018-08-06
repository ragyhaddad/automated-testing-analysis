#!/bin/bash/Python
#Usage: ./runRegression.py <input.csv> or <input-directory>
#Add the functions you want at the end of the script in the Driver section
import pandas as pd
import numpy as np 
import seaborn as sns; sns.set()
from sklearn import linear_model
import sys
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import statsmodels.formula.api as sm
from sklearn.cross_validation import train_test_split


# Global Variables
df = 0
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
r_score = 0
fail_differences = []
X_opt = 0
regressor_OLS = 0
multi_dimensions = []
#Option for dropping nulls in dataframe
dropna = True

#PDF to save data
pp = PdfPages('regression.pdf')

#Functions


#Reads file and creates a dataframe
# @param - (String)
def readFile(file_path):
    global df
    df = pd.read_csv(file_path,skiprows=[1])

    if(dropna == True):
        df = df.dropna()  #Important drops null values in each column
    #Remove last line 
    df = df.drop(df.index[len(df)-1])
   

#Split function
# @param - (int,int,int,int)
def split(x_col, y_col, percent_train=100, percent_test=100):
    global X , Y, X_train, Y_train, X_test, Y_test, df
    X = df.iloc[:,x_col].values.reshape(-1,1)
    Y = df.iloc[:,y_col].values.reshape(-1,1)
    split_percent = int((float(percent_train)/100) * len(X)) -1
    test_percent = int((float(percent_test)/100) * len(Y)) -1
    X_train = X[:-split_percent]
    X_test = X[-test_percent:]
    Y_train = Y[:-split_percent]
    Y_test = Y[-test_percent:]


#Multiple regression splitting
# @param - ([multi_variables],Y, int,int)
def splitMulti(x_col,y_col):
    global X , Y, X_train, Y_train, X_test, Y_test, df
    X = df.iloc[:, :-1].values

    Y = df.iloc[:,y_col].values

    
# Fit Regression Model
# @param - global variables
def runModel():
    global Y_predict, regr, r_score, X_opt
    X_opt = X[:,[0,1,2,3,4,5,6,7,8,9,10]]
    regr = linear_model.LinearRegression()
    regr.fit(X_train,Y_train)
    Y_predict = regr.predict(X_test)
    r_score = r2_score(Y_test, Y_predict)

def runMulitModel(X_options):
    global regressor_OLS, Y_test, Y_train, X_train
    X_opt = X[:,X_options]
    regressor_OLS = sm.OLS(endog = Y, exog = X_opt).fit()
    

# Plot Regression Line   
# @param - (int, int),  Column numbers
def plotModel(x,y):
    title = 'Bivariate fit ' + df.columns[x] +  ' and ' + df.columns[y]
    plt.title(title)
    plt.scatter(X_test, Y_test,  color='blue',alpha=0.5)
    plt.plot(X_test, Y_predict, color='black', linewidth=3)
    plt.show()
    
# Plot multiple figures in one page 
# - @param (int, String)
def plotMultiple(x,filename):
    title = 'Bivariate fit ' + df.columns[0] +  ' and ' + df.columns[9]
    fig.suptitle(title)
    sub_title = os.path.basename(filename) + ' Beta: ' + str(regr.coef_[0][0])
    axs[x].set_title(sub_title)
    axs[x].scatter(X_test, Y_test,  color='blue',alpha=0.5)
    axs[x].plot(X_test, Y_predict, color='black', linewidth=3)
    

# Reads a directory and populates an array of file names
# @param - (String)
def readDirectory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(os.path.join(directory, filename))
            file_path = os.path.join(directory,filename)
            file_array.append(file_path)
    return file_path
		

def createRegressionReport():
    count = 0
    #Create grif for subplots
    fig, axs = plt.subplots(2,2, figsize=(30, 20), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace =0.5, wspace=0.5)
    axs = axs.ravel()
    #Call read directory, - stores array of file names in global variable
    readDirectory(sys.argv[1])
    for x in range(24):
        readFile(file_array[x])
        split(0,9,20,80)
        runModel()
        plotMultiple(count,file_array[x])
        count = count + 1
        if(count == 4):
            fig.savefig(pp,format='pdf',dpi=10)
            fig, axs = plt.subplots(2,2, figsize=(30, 20), facecolor='w', edgecolor='k')
            fig.subplots_adjust(hspace =0.5, wspace=0.5)
            axs = axs.ravel()
            count = 0
    pp.close()


def findBestPredictor(dimensions_array,no_dimensions):
    temp_coef = 0
    temp_x = 0
    temp_y = 0
    r_temp = 0
    for x in range(len(dimensions_array)):
        for y in range(len(dimensions_array)):
            if (x == y):
                continue
            else:
                split(x,y,20,80)
                runModel()
                if(r_score > r_temp):
                    temp_coef = regr.coef_[0][0]
                    temp_x = x
                    temp_y = y
                    r_temp = r_score
        
        print temp_x,'\t',temp_y,'\t',temp_coef,'\t' ,r_temp
        temp_coef = 0
        temp_x = 0
        temp_y = 0
        r_temp = 0

#Calculates the difference between two columns
def calculateFailureDifference(x,y):
    global fail_differences
    for file in file_array:
        readFile(file)
        print df.iloc[:,3].isnull().sum(),'\t', df.iloc[:,4].isnull().sum()
        difference = abs(df.iloc[:,x].isnull().sum() - df.iloc[:,y].isnull().sum())
        fail_differences.append(difference)


def plotDifferences():
    readDirectory(sys.argv[1])
    xcol = 5
    ycol = 6
    calculateFailureDifference(xcol, ycol)
    suptitle = 'Failed tests comparison between test ' + str(xcol)   + ' and ' + str(ycol)
    plt.suptitle(suptitle)
    title = 'Average failure difference: ' + str(sum(fail_differences)/len(fail_differences))
    plt.title(title)
    plt.plot(fail_differences)
    plt.xticks(np.arange(len(file_array)))
    plt.show()




