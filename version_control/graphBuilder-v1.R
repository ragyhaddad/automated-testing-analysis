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

if(length(args) < 3){
	write('Usage: Rscript graphBuilder-v1.R <input.csv> <output.pdf> <no_of_rows_to_skip>',stdout())
	quit()
}

#Input File
inputFile = args[1]

#Column numnber to plot
# columnNumber = as.numeric(args[2])

grobList = list()
#Output File

outputName = paste(args[2])


pdf(outputName,onefile=TRUE)

length_1 = as.numeric(nchar(inputFile))
length_2 = nchar(outputName)
skip = args[3]


#DataFrame
df = read.csv(inputFile, header=TRUE, check.names=FALSE, sep=",",skip=skip)

#Drop uneeded columns --> only process tests
# drops = c("X","Y","Elapsed Time","LOT_ID","JOB_NAM","Temperature")
# df = df[,!(names(df) %in% drops)]

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
	 text = element_text(size=9,face='bold'))


#Parse test name @param - string, number of chars from back
substrRight = function(x, n){
  substr(x, nchar(x)-n+1, nchar(x))
}


#Test limits @param - testName
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
	if(test_number == 302){
		min_limit = -1.5
		max_limit = -0.5
		units = '(m)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 303){
		min_limit = -1.5
		max_limit = -0.5
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
		min_limit = 1.1399999856948853
		max_limit = 1.350000023841858
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
		min_limit = 900000.0
		max_limit = 1100000.0
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
		min_limit = -0.5
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
	if(test_number == 330){
		min_limit = 130.0
		max_limit = 130.0
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 331){
		min_limit = 0
		max_limit = 255
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 332){
		min_limit = 131.0
		max_limit = 131.0
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 333){
		min_limit = 131.0
		max_limit = 131.0
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	##334
	if(test_number == 334){
		min_limit = 129
		max_limit = 129
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 338){
		min_limit = 130
		max_limit = 130
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
	if(test_number == 340){
		min_limit = 2.4
		max_limit = 2.6
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 337){
		min_limit = -0.009999999776482582
		max_limit = 0.029999999329447746
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
	if(test_number == 335){
		min_limit = 2.0
		max_limit = 2.0
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}
	if(test_number == 336){
		min_limit = -0.009999999776482582
		max_limit = 0.029999999329447746
		units = '(V)'
		limits = c(min_limit,max_limit,units)
		return(limits)
	}


	else{
		min_limit = 0
		max_limit = 0
		limits = c(min_limit,max_limit,units)
		return(limits)
	}

}


#Function to plot @params - Column Number from CSV file 
plotGraphArray = function(input){
	#Get column from dataframe
	dataColumn = df[,input]
	
	columnName = colnames(df[input])
	
	#Get limits
	limits = getTestLimits(columnName)

	##Max and min limits
	max = as.double(limits[2])
	min = as.double(limits[1])



	#Scale Delta for limits
	scale_delta = (max - min)*1.5
	
	#Handle same limits
	if(max == min){
		scale_delta = 0.5 * max	
		if(scale_delta == 0){
			min = min(dataColumn,na.rm=TRUE)
			max = max(dataColumn,na.rm=TRUE)
			scale_delta = 0.5 * max
			max = as.double(limits[2])
			min = as.double(limits[1])
		}
	}
	
	#X limits
	x_label = paste('Measured Value ',limits[3])


	#Translate out of bounds data to max and min bins
	dataColumn[dataColumn < min] = (min - (scale_delta*0.9))
	dataColumn[dataColumn > max] = (max + (scale_delta*0.9))	
	



	#Histogram 1
	histo = ggplot(df,aes(dataColumn)) +
	geom_histogram(bins=100,col=I('black'),fill=I('blue')) +
		   scale_x_continuous(limits = c((min - scale_delta), (max + scale_delta))) +
		   		xlab(x_label) + gridTheme +
		    		geom_vline(xintercept=min, linetype='dashed', color="red") +
		    			geom_vline(xintercept=max, linetype='dashed', color="red")

	#Summary 1
	summary = as.matrix(summary(dataColumn))

	#Arrange layout
	return(list(histo,summary,columnName))
	
	
}


#Starting Column
x = 1

#Number of columns in DF
totalColumns = ncol(df)

#Grob array
grobs = list()

#Create Grobs in an array
while(x < totalColumns){
	grobs[[x]] = plotGraphArray(x)
	x = x + 1
}
#Prompt Number of tests
print('Number of Tests:')
print(x)
print(totalColumns)

#Reset Index
x = 1

print('Generating file...')

#Generate all graphs 

	#Plot grobs on PDF
while(x < totalColumns){
	table_1 = tableGrob(grobs[[x]][[2]], theme=tt3, cols=grobs[[x]][[3]])
	table_2 = tableGrob(grobs[[x+1]][[2]], theme=tt3, cols=grobs[[x+1]][[3]])
	table_3 = tableGrob(grobs[[x+2]][[2]], theme=tt3, cols=grobs[[x+2]][[3]])
	graph_1 = grobs[[x]][[1]]
	graph_2 = grobs[[x+1]][[1]]
	graph_3 = grobs[[x+2]][[1]]
	grid.arrange(table_1,graph_1,table_2,graph_2,table_3,graph_3,ncol=2,nrow=3)	
	x = x + 3
	# print(x)
}





##DONE
print('Generated histograms: ')
print(outputName)





