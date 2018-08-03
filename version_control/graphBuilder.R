#!/bin/bash/Rscript
library(grid)
library(gridExtra)
library(ggplot2)
library(pastecs)
library(gridGraphics)
library(scales)
library(ggthemes)
#System args
args = commandArgs(trailingOnly=TRUE)

#Input File
inputFile = args[1]

#Column numnber to plot
columnNumber = as.numeric(args[2])

#Output File
pdf('graphBuilder_ouput.pdf',onefile=TRUE)

#DataFrame
df = read.csv(inputFile, header=TRUE, check.names=FALSE, sep=",")


#Table theme
tt3 = gridExtra::ttheme_default(
    core = list(fg_params=list(cex = 0.7,hjust=0, x=0.1)),
    colhead = list(fg_params=list(cex = 0.7)),
    rowhead = list(fg_params=list(cex = 0.7)))

	

#Histogram Theme
gridTheme = theme(panel.grid.major = element_line(colour = 'grey20', linetype = 'dotted')
	,panel.grid.minor = element_line(colour = NA),
	 panel.background = element_rect(fill= 'white'),
	 axis.ticks = element_line(colour = "black"),
	 axis.line = element_line(colour='black'),
	 text = element_text(size=9))




#Parse test name to find test number
substrRight = function(x, n){
  substr(x, nchar(x)-n+1, nchar(x))
}

##Summary
summaryfun <- function(x)list(N=length(x),Mean=mean(x),Median=median(x),SD=sd(x),Min=min(x),Max=max(x))




#Test limits
getTestLimits = function(testName){
	print(testName)
	units = ''
	test_number = substrRight(testName,3)
	if(test_number >= 100 && test_number <= 109 ){
		min_limit = -0.725
		max_limit = -0.500
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 200){
		min_limit = -1 * (10^-7)
		max_limit = 1 * (10^-7)
		units = '(A)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 201){
		min_limit = -0.000039999999999999996
		max_limit = 0.000039999999999999996
		units = '(A)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}	
	if(test_number >= 202 && test_number <= 205 ){
		min_limit = -0.000009999999999999999
		max_limit = 0.000009999999999999999
		units = '(A)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 300){
		min_limit = 53
		max_limit = 53
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 301){
		min_limit = 52
		max_limit = 52
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number >= 302 && test_number <= 303 ){
		min_limit = -1.5
		max_limit = -500
		units = '(m)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 304){
		min_limit = 0.002
		max_limit = 0.0035
		units = '(A)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 305){
		min_limit = 0.024
		max_limit = 0.03
		units = '(A)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 306){
		min_limit = 3.28
		max_limit = 3.46
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 307){
		min_limit = 2.4
		max_limit = 2.6
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 308){
		min_limit = 1.14
		max_limit = 1.35
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 309 || test_number == 310){
		min_limit = -0.005
		max_limit = 0.02
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 311 || test_number == 312){
		min_limit = 1.8
		max_limit = 2.15
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 313){ ##Clock frequency
		min_limit = 1100000 
		max_limit = 900000000
		units = '(Hz)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 314){
		min_limit = 1.08
		max_limit = 1.32
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 315){
		min_limit = 0
		max_limit = 15
		units = ''
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 316){
		min_limit = -500
		max_limit = 5.5
		units = ''
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 317){
		min_limit = 0
		max_limit = 3
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 318){
		min_limit = 0
		max_limit = 6
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 319){
		min_limit = -30
		max_limit = 30
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 320){
		min_limit = -30
		max_limit = 6
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 321){
		min_limit = 14
		max_limit = 22
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 322){
		min_limit = -30
		max_limit = 30
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}

	if(test_number == 323){
		min_limit = -30
		max_limit = 6
		units = '(dB)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 324){
		min_limit = 0
		max_limit = 0
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 325){
		min_limit = 0
		max_limit = 15
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 326){
		min_limit = 2
		max_limit = 2
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 327){
		min_limit = 130
		max_limit = 130
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 328){
		min_limit = 131
		max_limit = 131
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 329){
		min_limit = -20
		max_limit = 5
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 330 || test_number == 332 || test_number == 333 || test_number ==337){
		min_limit = 130
		max_limit = 130
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 331){
		min_limit = 0
		max_limit = 255
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	##334
	if(test_number == 334 || test_number == 338){
		min_limit = 2
		max_limit = 2
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 339){
		min_limit = 0
		max_limit = 140
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 338){
		min_limit = 2
		max_limit = 2
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number >= 335 && test_number <= 336 ){
		min_limit = -0.01
		max_limit = 0.03
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}

	else{
		min_limit = -0.725
		max_limit = -0.500
		limits = c(min_limit,max_limit)
		return(limits)
	}

}


#Function to plot @params - Column Number from CSV file 
plotGraph = function(input){

	#Get column from dataframe
	dataColumn = df[,input]
	dataColumn_2 = df[,input +1]
	columnName = colnames(df[input])
	columnName_2 = colnames(df[input+1])

	#Get min and max
	limits = getTestLimits(columnName)
	limits_2 = getTestLimits(columnName_2)


	##Max and min limits
	max = as.double(limits[2])
	min = as.double(limits[1])
	max_2 = as.double(limits_2[2])
	min_2 = as.double(limits_2[1])


	
	#Scale Delta for limits
	scale_delta = (max - min)
	scale_delta_2 = (max_2 - min_2)

	#Handle same limits
	if(max == min){
		scale_delta = 0.5 * max	
	}
	if(max_2 == min_2){
		scale_delta_2 = 0.5 * max_2
	}
	
	x_label = paste('Measured Value ',limits[3])
	x_label_2 = paste('Measured Value ',limits[3])
	#Histogram 1
	histo = ggplot(df,aes(dataColumn)) +
	geom_histogram(bins=100,col=I('black'),fill=I('blue')) +
		   scale_x_continuous(limits = c((min - scale_delta), (max + scale_delta))
		   	) +
		    xlab(x_label) + gridTheme +
		    	geom_vline(xintercept=min, linetype='dashed', color="red") +
		    		geom_vline(xintercept=max, linetype='dashed', color="red")
	
	#Histogram 2
	histo_2 = ggplot(df,aes(dataColumn_2)) +
	geom_histogram(bins=100,col=I('black'),fill=I('blue')) +
		   scale_x_continuous(limits = c(min_2 - scale_delta_2,max_2 + scale_delta_2)) +
		    xlab(x_label_2) + gridTheme+
		    	geom_vline(xintercept=min_2, linetype='dashed', color="red") +
		    		geom_vline(xintercept=max_2, linetype='dashed', color="red")
	#Summary 1
	summary = as.matrix(summary(dataColumn))
	#Summary 2
	summary_2 = as.matrix(summary(dataColumn_2))
	#Arrange layout
	grid.arrange(tableGrob(summary,theme=tt3,cols = columnName),histo,tableGrob(summary_2,theme=tt3,cols = columnName_2),histo_2,ncol=2,nrow=3,top="Sample Test Distribution Report")
	
}

x = 2
#Number of columns in DF
totalColumns = ncol(df)
#Call Function
while(x < totalColumns){
	plotGraph(x)
	x = x + 2
}

#Test limits
getTestLimits = function(testName){
	print(testName)
	test_number = substrRight(testName,3)
	print(test_number)
	if(test_number >= 100 && test_number <= 109 ){
		min_limit = -0.725
		max_limit = -0.500
		limits = c(min_limit,max_limit)
		print(limits)
		return(limits)
	}
	if(test_number == 200){
		min_limit = -0.1 * (10^-7)
		max_limit = 0.1 * (10^-7)
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 201){
		min_limit = -0.000039999999999999996
		max_limit = 0.000039999999999999996
		limits = c(min_limit,max_limit)
		return(limits)
	}	
	if(test_number >= 202 && test_number <= 205 ){
		min_limit = -0.000009999999999999999
		max_limit = 0.000009999999999999999
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 300){
		min_limit = 0
		max_limit = 53
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 301){
		min_limit = 0
		max_limit = 52
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number >= 302 && test_number <= 303 ){
		min_limit = -1.5
		max_limit = -500
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 304){
		min_limit = 0.02
		max_limit = 0.035
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 305){
		min_limit = 0.024
		max_limit = 0.03
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 306){
		min_limit = 3.28
		max_limit = 3.46
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 307){
		min_limit = 2.4
		max_limit = 2.6
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 308){
		min_limit = 1.14
		max_limit = 1.35
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 309 || test_number == 310){
		min_limit = -0.005
		max_limit = 0.02
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 311 || test_number == 312){
		min_limit = 1.8
		max_limit = 2.15
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 313){ ##Clock frequency
		min_limit = 900000000
		max_limit = 1100000
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 314){
		min_limit = 1.08
		max_limit = 1.32
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 315){
		min_limit = 0
		max_limit = 15
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 316){
		min_limit = -500
		max_limit = 5.5
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 317){
		min_limit = 0
		max_limit = 3
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 318){
		min_limit = 0
		max_limit = 6
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 319){
		min_limit = -30
		max_limit = 30
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 320){
		min_limit = -30
		max_limit = 6
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 321){
		min_limit = 14
		max_limit = 22
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 322){
		min_limit = -30
		max_limit = 30
		limits = c(min_limit,max_limit)
		return(limits)
	}

	if(test_number == 323){
		min_limit = -30
		max_limit = 6
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 324){
		min_limit = 0
		max_limit = 0
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number == 325){
		min_limit = 0
		max_limit = 15
		limits = c(min_limit,max_limit)
		return(limits)
	}
	if(test_number >= 339 && test_number <= 340 ){
		min_limit = 2.4
		max_limit = 2.6
		limits = c(min_limit,max_limit)
		print(limits)
		return(limits)
	}
	if(test_number == 338){
		min_limit = 0
		max_limit = 2
		limits = c(min_limit,max_limit)
		print(limits)
		return(limits)
	}
	if(test_number >= 335 && test_number <= 336 ){
		min_limit = -0.01
		max_limit = 0.03
		limits = c(min_limit,max_limit)
		print(limits)
		return(limits)
	}

	else{
		min_limit = -0.725
		max_limit = -0.500
		limits = c(min_limit,max_limit)
		return(limits)
	}

}


