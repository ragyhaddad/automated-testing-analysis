#!/bin/bash/env python
#Author: Ragy Haddad
#Parser from open-source libstdf_dump_to_ascii output to csv.

import sys
import os
import re


if(len(sys.argv) < 1):
	print("Usage: python stdf2csv.py <input file generated from libstdf>")


## System Args
file_path = sys.argv[1]

output_file_name = "outcsv-v5.csv"
## Write output to file
output_file = open(output_file_name,"w")

## Load file content to array
with open(file_path) as f:
    content = f.readlines()

print("Number of records in ASCII out from libstdf:")
print(len(content))
print("Exporting to CSV...")
## Global Variables
count = 0
count_header = 0
row = ""
header_row = ""
header_array = []
row_array = []
count_header = 0
header_row = ""

# Loops over first set of tests and records header names
for line in content:
	test_record = re.search('Record PTR', line)
	record_end = re.search('Record EPS', line)
	if(test_record):
		grep_result = re.search('(TEST_TXT): (.+)', content[count_header + 7])
		header_row = header_row + grep_result.group(2) + ','
		# header_array.append(grep_result.group(2)) 
	if(record_end):
		row = row + header_row
		output_file.write(row)
		output_file.write('\n')
		row = ""
		break
	count_header = count_header + 1

# Loop over content and parse each record for each wafer
for x in range(len(content)):
	line = content[x]
	test_record = re.search('PTR', line) ## Parametric Test record
	record_start = re.search('PIR', line) ## 
	record_end = re.search('PRR', line) ## End of Record per wafer
	if(record_start):
		
		row = ""
		record_start = True
	elif(record_end):
		count = 0
		record_end = True
		output_file.write(row)
		output_file.write('\n')
	elif(test_record):
		grep_result = re.search('(RESULT): (.+)', content[x + 6])
		result = grep_result.group(2)
		if(len(result) == 0):
			result = 'NA'
		row = row + result + ','


## User prompt
print("CSV generated!")
print("Output file:")
print(output_file_name)


	
	


	

