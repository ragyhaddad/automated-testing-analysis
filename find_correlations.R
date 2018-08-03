#!/usr/bin/Rscript
#System args
#Usage: Rscript find_correlations.R <no_rows_to_skip> <correlation_coefficient_cuttoff>

args = commandArgs(trailingOnly=TRUE)

#Command line args
filename = args[1]
skipRows = args[2]
cutoff = args[3]
if(length(args) < 3){
	write('Rscript find_correlations.R <in.csv> <no_rows_to_skip> <correlation_coefficient_cuttoff>',stdout())
	quit()
}
#Remove Scientific notation
options(scipen=999)

#Read Data
data = read.csv(filename,check.names=FALSE, header=TRUE,skip = skipRows)

#Number of columsn in dataframe
columns = ncol(data)

#Find correlation between two columns
findCorrelation = function(col1,col2){
	columnOne = data[col1]
	columnTwo = data[col2]
	if(colnames(columnOne) == 'Time' || colnames(columnTwo) == 'Time'){
		return()
	}
	if( is.numeric(data[,col1]) && is.numeric(data[,col2]) ){
		correlation = cor(columnOne, columnTwo,use = 'complete.obs')
		output = paste(colnames(columnOne),',',colnames(columnTwo),',',correlation[1])
		if(as.numeric(correlation[1]) >= cutoff){
			if(correlation[1] > 0 && correlation[1] < 1){
				write(output, stdout())
			}
			
		}
		
	}
}

x = 1;
y = 1;
correlationArray = list()
combinations = c()
#Header
header = paste('Test 1 Name',',','Test 2 Name',',','Correlation Co-efficient')
write(header, stdout())
#Loop over columns
while( x < columns){
	while(y < columns){
		comb = paste(x,'-',y)
		rev_comb_temp = paste(y,'-',x)
		
		if(comb %in% combinations == FALSE && rev_comb_temp %in% combinations == FALSE){
			combinations = c(combinations,comb)
			combinations = c(combinations,rev_comb_temp)
			if(x != y){
				correlation = findCorrelation(x,y)
			}
			
		}
		y = y + 1
	}
	x = x + 1
	y = 1
}


