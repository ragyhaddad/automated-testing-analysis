#!/bin/bash/python
#Usage: python runPCA.py <input.csv>
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns; sns.set()
import numpy as np
from sklearn.datasets import load_digits
from matplotlib.backends.backend_pdf import PdfPages
import itertools
import scipy.stats as stats
import os
from sklear.cross_validation import train_test_split

##Testing mode
df = 0
columnOne = 0
pca = 0
transformed_data = 0
inverse = 0
multi_mode = False
dimensions = []
inverse_df = 0

#Batch mode
batch_mode = True


#PDF for saving plots
pp = PdfPages('multipage_all.pdf')
pp2 = PdfPages('multipage.pdf')
myarray = []
max_differences = []
# @param: file_input and creates a df
def readFile(file_path):
	global df, columnOne, pca,transformed_data,inverse_transform
	df = pd.read_csv(file_path,skiprows=[1])
	df = df.dropna()
	columnOne = 0
	pca = 0
	transformed_data = 0
	multi_mode = False
	# dfrm.drop(dfrm.index[len(dfrm)-1])


#Run pca - params int col_1, int col_2
def runPCA(x,y):
	global columnOne,pca,transformed_data,inverse
	columnOne = df.iloc[0:,[x,y]]
	pca = PCA(n_components=1)
	pca.fit(columnOne)
	print(pca.explained_variance_ratio_)
	transformed_data = pca.transform(columnOne)
	inverse = pca.inverse_transform(transformed_data)
	return pca.explained_variance_ratio_

#Runs multidimensional PCA, flexible mode for PCA.
# @param: variable [array], no_components [int], threshold (float) 
def runPCAFlex(dimensions_array, no_components):
	global columnOne,pca,transformed_data,inverse
	columnOne = df.iloc[0:,dimensions_array]
	pca = PCA(n_components=no_components)
	pca.fit(columnOne)
	print(pca.explained_variance_ratio_)
	transformed_data = pca.transform(columnOne)
	inverse = pca.inverse_transform(transformed_data)

#Explore the dimensionality reduction of the data - USE ONE COMPONENET.
def reduction():
	title = 'Dimensionality Reduction between test '+columnOne.columns[0]+ ' VS ' + columnOne.columns[1]
	plt.suptitle(title, fontsize=16)
	eigen_value = 'Eigen Value: '+ str(round(pca.explained_variance_ratio_[0]*100,4))
	plt.title(eigen_value)
	plt.scatter(columnOne.iloc[:,0],columnOne.iloc[:,1],c='c',alpha=0.3)
	plt.scatter(inverse[:,0],inverse[:,1],c='b',alpha=0.8)
	plt.axis('equal');
	filename = str(columnOne.columns[0]) + str(columnOne.columns[1]) 
	plt.savefig(pp2,format='pdf')
	filename = 'PCA_reduction/'+filename
	plt.clf()

#Draw a regular Scatter plot for PCA transformation
def scatterComponents():
	global myarray
	title = 'Number of components: ' + str(len(myarray))
	labels = np.asarray(columnOne.columns)
	plt.suptitle(labels, fontsize=16)
	eigen_value = 'Eigen Value: '+ str(round(pca.explained_variance_ratio_[0]*100,4))
	plt.title(eigen_value)
	scatter = plt.scatter(transformed_data[:,0],transformed_data[:,1],c=['b','c'],alpha=0.5)
	plt.axis('equal')
	xlabel = 'principal component 1 (' + str(round(pca.explained_variance_ratio_[0]*100,4)) +' %)'
	ylabel = 'principal component 2 (' + str(round(pca.explained_variance_ratio_[1]*100,4)) +' %)'
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	

#Draw PCA Vectors
def draw_vector(v0,v1, ax = None):
	ax = ax or plt.gca()
	arrowprops=dict(arrowstyle='->',linewidth=2,shrinkA=0,shrinkB=0)
	ax.annotate('',v1,v0,arrowprops=arrowprops)



#Create all 2-dimensional reductions and plot to output
# @param: threshold (cuttoff for eigen value) [float]
def createReductions(threshold):
	store_combination = []
	for x in range(10):
		for y in range(10):
			combination = str(x) + str(y)
			reverse_combination = str(y) + str(x)
			if(combination in store_combination or reverse_combination in store_combination):
				continue

			if(x == y):
				continue
			else:
				eigen_value = runPCA(x,y)
				if(eigen_value > threshold):
					reduction()
					store_combination.append(combination)
					store_combination.append(reverse_combination)

	pp2.close()



#Create all dimensions itterate till two PCA
def runPCAAnalaysis(dimensions_array):
	dimensions = dimensions_array
	runPCAFlex(dimensions_array,2)
	scatterComponents()
	


#Run PCA analysis on an array of variables
def getAllPCA(no_dimensions):
	combinations = list(itertools.combinations(dimensions,no_dimensions))
	for x in range (len(combinations)):
		myarray = np.asarray(combinations[x]) 
		runPCAAnalaysis(myarray)




#runs PCA flex with dimensions and back projects on given file
def fitFile():
	global dimensions, inverse_df, inverse_transform, transformed_data
	dimensions = [0,1,2,3,4,5,6,7,8,9]
	runPCAFlex(dimensions,6)
	inverse_transform = pca.inverse_transform(transformed_data)
	inverse_df = pd.DataFrame(inverse_transform)


def backProject(column_one,column_two):
	plt.clf()
	inverse_transform = pca.inverse_transform(transformed_data)
	# plt.axis('equal')
	print('original shape',columnOne.shape)
	print('transformed shape', transformed_data.shape)
	print('reconstruction',inverse_transform.shape)
	
	transformed_df = pd.DataFrame(transformed_data)
	plt.title('reconstructing original data using 6 components')
	plt.scatter(columnOne.iloc[:,column_one],columnOne.iloc[:,column_two],label='original',color='b',alpha=0.5)
	plt.scatter(inverse_transform[:,column_one],inverse_transform[:,column_two],label='reconstruction from pca',color='red',alpha=0.3)
	plt.legend()

	plt.show()


#Gets the mean error between original and backprojection
def meanError():
	difference_array = []
	global max_differences
	for x in range(len(dimensions)):
		mean_error = abs((columnOne.iloc[:,x] - inverse_df.iloc[:,x])).mean()
		difference_array.append(mean_error)

	print(difference_array)
	print(max_differences)
	if (len(max_differences) == 0 ):
		max_differences = difference_array
	for x in range(len(difference_array)):
		if(difference_array[x] < max_differences[x]):
			max_differences[x] = difference_array[x]


	# plt.show()

def plotMeanError(mean_difference):
	global dimensions
	print('Plotting max difference')
	print(mean_difference)
	print(dimensions)
	mean_title = 'Minimum Mean absolute error of each back projection from PCA '
	plt.title(mean_title)
	plt.xlabel('Test Number')
	plt.ylabel('Mean absolute Error')
	plt.plot(dimensions,mean_difference)
	plt.xticks(dimensions)
	plt.show()


#plots a histogram of difference
def histogramError(column_no):
	difference_column = columnOne.iloc[:,column_no] - inverse_df.iloc[:,column_no]
	plt.hist(difference_column.dropna(),edgecolor='black',linewidth=0.5,bins=100)
	title = 'Error distribution from 6 -> 10 back projection'
	suptitle = 'Test Number: 10' +str(column_no) 
	plt.suptitle(suptitle)
	plt.title(title)
	plt.xlabel('Measured Error')
	plt.ylabel('Distribution')
	# plt.show()

#Plot histograms on one another for backprojected data
def backProjectHistogram(column_no):
	plt.hist(columnOne.iloc[:,column_no],edgecolor='black',linewidth=0.5,color='blue',bins=300)
	plt.hist(inverse_transform[:,column_no],edgecolor='black',linewidth=0.5,color='r',bins=300,alpha=0.4)
	plt.legend()
	plt.show()

#Should delete this one same as previous
def backProjectNormal(column_no):
	plt.plot(columnOne,color='b',label='original')
	plt.plot(inverse_transform,color='red',label='reconstruction',alpha = 0.5)
	plt.show()






		# meanError()














	







