#!/bin/bash/python
#Usage: python findOptimalComponents.py <input.csv>
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns; sns.set()
import sys


file = sys.argv[1]
data = pd.read_csv(file,skiprows=[0])
data = data.dropna()
dimensions_array = [0,1,2,3,4,5,6,7,8,9]
# dimensions_array = [0,2,7,8,9]
dimensions_array = [3,4,5]
n_components = len(dimensions_array)
reversedarray = [9,8,7,6,5,4,3,2,1,0]
xticks_array = [1,2,3,4,5,6,7,8,9,10]
pca = PCA(n_components=n_components)
columns = data.iloc[:,dimensions_array]
print columns.columns

pca.fit(columns)

print(pca.explained_variance_ratio_)

print(np.cumsum(pca.explained_variance_ratio_))

max_eigen = max(pca.explained_variance_ratio_)
min_eigen = min(pca.explained_variance_ratio_)
#Find cumalitive frequency.
def cumalitiveVariance():
	title = str(n_components) + ' continuity tests principal component breakdown'
	plt.title(title)
	plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='.',color='blue')
	plt.hlines(y=1, xmin=0, xmax=10,linestyle='--', color='darkorange', zorder=1)
	plt.xlabel('number of components')
	plt.ylabel('cumulative explained variance')
	plt.xticks(xticks_array)
	plt.show()

#Find log scale eigen
def eigenDistribution():
	plt.title('Eigen value distribution log scale')
	plt.plot(dimensions_array,pca.explained_variance_ratio_,linestyle='--', marker='o')
	plt.xlabel('principal component')
	plt.ylabel('eigen value')
	plt.yscale('log')
	plt.xticks(dimensions_array)
	plt.show()




eigenDistribution()









