#!/bin/bash/env python
import sys
import pandas as pd 
import numpy as np
import statsmodels.api as sm 
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

if(len(sys.argv) < 2):
    print 'Usage: python multipleRegression.py <tests_input.csv>'
    sys.exit(1)


#Import data
df = pd.read_csv(sys.argv[1], skiprows=[1])
df = df.dropna()
df = df.head(2000)

df = df.drop(df.index[len(df)-1])

#Model and predictions
predictors = [1,3,4,5]
dependant_variable = 9
print df.iloc[:,predictors].columns
X = df.iloc[:,predictors].values
Y = df.iloc[:,dependant_variable].values
X = sm.add_constant(X)
results = sm.OLS(exog = X, endog = Y).fit()
predict_y = results.predict(X)

compare_df = pd.DataFrame({'Original':Y, 'Predicted':predict_y})
print compare_df
print results.summary()






