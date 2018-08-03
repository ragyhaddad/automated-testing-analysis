#!/usr/bin/env Rscript

# Author: Ragy Haddad
# Summary: Script for plot summary and test distributions for stdf testing data.
# Usage: Rscript stdf_distribution.R <filename> <column_number>
# Where column number is the column number in the csv file you wish to plot


# Libraries
library(grid)
library(gridExtra)
library(ggplot2)
library(devtools)
library(gridGraphics)
library(pastecs)
# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)
filePath = args[1]
columnNumber = as.numeric(args[2])

outputName = paste(args[3],'.pdf')

# PDF to save output
pdf(outputName, onefile = TRUE)

# Comment for processing the file
sprintf('Processing: %s .....', filePath) 

# Load data frame
mydata = read.csv(filePath, header=TRUE, check.names = FALSE, sep=',')
original_data = read.csv('/Users/ragyhaddad/Desktop/original_final.csv',header=TRUE,check.names=FALSE,sep=',',skip=1)
#table theme
tt3 <- gridExtra::ttheme_default(
    core = list(fg_params=list(cex = 0.7,hjust=0, x=0.1)),
    colhead = list(fg_params=list(cex = 0.7)),
    rowhead = list(fg_params=list(cex = 0.7)))



# Theme for column
tt = ttheme_default(colhead=list(fg_params = list(parse=TRUE)))
# layout(matrix(c(1,1,2,3), 2, 2, byrow = TRUE), 
#   	widths=c(1,1), heights=c(1,1))
drawPlot = function(x){
	#Find column mean
	dataColumn = mydata[,x]
	column_name_1 = colnames(mydata[x])
	
	x_original = which(colnames(original_data) == column_name_1 )
	dataColumnOriginal = original_data[,x_original]

	print(column_name_1)
	print(colnames(original_data[x_original]))


	max = max(dataColumn,na.rm=TRUE)
	min = min(dataColumn,na.rm=TRUE)
	mean = mean(dataColumn, na.rm=TRUE)
	print(summary(dataColumn))
	print(summary(dataColumnOriginal))
	print(min)
	print(max)

	#Graph plotting
	graphPlot = ggplot(mydata,aes(dataColumn)) +
	geom_freqpoly(binwidth = 0.01,bins=200,color="navyblue", fill="blue") + 
	labs(x = 'measured value') + theme_bw()

	graphPlotOriginal = ggplot(original_data,aes(dataColumnOriginal,'1')) +
	geom_freqpoly(binwidth = 0.01,bins=200,color="navyblue", fill="red") + 
	labs(x = 'measured value') + theme_bw()
	print(graphPlotOriginal)
	print(graphPlot)

	label_1 = paste(colnames(mydata[x]),"\nNew Parser")
	label_2 = paste(colnames(mydata[x]),"\nOriginal Data")
	summary_original = as.matrix(summary(dataColumnOriginal))
	summary = as.matrix(summary(dataColumn))
	test_label = textGrob(label_1, gp = gpar(family='symbol',fontsize = 8, col = 'black', fontface = 'bold'))
	test_label_original = textGrob(label_2, gp = gpar(family='symbol',fontsize = 8, col = 'black', fontface = 'bold'))
	summary_table = tableGrob(summary, theme=tt3)
	summary_table_original = tableGrob(summary_original,theme=tt3)
	right_label = textGrob("Parser output")
	grobs = c(test_label,right_label,graphPlot,summary_table)

	grid.arrange(test_label,graphPlot,summary_table,test_label_original,graphPlotOriginal,summary_table_original,nrow=3,ncol = 3,top = textGrob("STDF to CSV Parser Performance",gp=gpar(fontsize=16)))
}

# Call the function on the column number
# drawPlot(columnNumber)


plotSummaryTable = function (x){

	dataColumn = mydata[,x]
	column_name_1 = colnames(mydata[x])
	
	x_original = which(colnames(original_data) == column_name_1 )
	dataColumnOriginal = original_data[,x_original]

	print(column_name_1)
	print(colnames(original_data[x_original]))

	max = max(dataColumn,na.rm=TRUE)
	min = min(dataColumn,na.rm=TRUE)
	mean = mean(dataColumn, na.rm=TRUE)
	print(summary(dataColumn))
	print(summary(dataColumnOriginal))
	print(min)
	print(max)
	label_1 = paste("New Parser")
	label_2 = paste("Original Data")

	test_label = textGrob(label_1, gp = gpar(family='symbol',fontsize = 8, col = 'black', fontface = 'bold'))
	test_label_original = textGrob(label_2, gp = gpar(family='symbol',fontsize = 8, col = 'black', fontface = 'bold'))

	summary = stat.desc(mydata[column_name_1])
	summary_original = stat.desc(original_data[column_name_1])
	summary_table = tableGrob(summary,theme=tt3)
	summary_table_original = tableGrob(summary_original,theme=tt3)

	grid.arrange(test_label,test_label_original,summary_table,summary_table_original,nrow=3,ncol = 2,top = textGrob("STDF to CSV Parser Performance/Summary Tables",gp=gpar(fontsize=16,cex=0.7)))
}


findMaxDiff = function(x){
	dataColumn = mydata[,x]
	column_name_1 = colnames(mydata[x])
	x_original = which(colnames(original_data) == column_name_1 )
	dataColumnOriginal = original_data[,x_original]
	diff = max(abs(dataColumn - dataColumnOriginal),na.rm=TRUE)
	diff_df = dataColumn - dataColumnOriginal
	columnMaxDiff = which.max(diff_df)
	print('Max row')
	print(columnMaxDiff)
	print(column_name_1)
	print(summary(dataColumn))
	print(colnames(original_data[x_original]))
	print(summary(dataColumnOriginal))
	print(diff)
}



findMaxDiff(columnNumber)







