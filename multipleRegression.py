#!/bin/bash/python
import sys
import pandas as pd 
import numpy as np
import statsmodels.api as sm 
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

#Import data
df = pd.read_csv(sys.argv[1], skiprows=[1])
df = df.dropna()
df = df.drop(df.index[len(df)-1])

#Model and predictions
predictors = [3,4,5,6,7,8,9]
dependant_variable = 0
print df.iloc[:,predictors].columns
X = df.iloc[:,predictors].values
Y = df.iloc[:,dependant_variable].values
X = sm.add_constant(X)
results = sm.OLS(exog = X, endog = Y).fit()
predict_y = results.predict(X)
print results.summary()




