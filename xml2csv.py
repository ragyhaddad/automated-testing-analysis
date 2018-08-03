#Author: Ragy Haddad
#Pipeline -> xml stdf to csv
#Takes in xml file from pystdf and converts it to csv

import xml.etree.ElementTree as ET
import csv
import sys
import re
import pandas as pd


print 'Importing file',sys.argv[1]

#Import/parse xml
tree = ET.parse(sys.argv[1])
root = tree.getroot()

#Open a file for writing
output_file = open(sys.argv[2], 'w')


#Create the csv writer object
csvwriter = csv.writer(output_file)

headers_arranged = ['LOT_ID','JOB_NAM','Temperature','X','Y','Elapsed Time']
columnNumber = 0

#Variables
count = 0
header = ""
rows = []
header_array = []
row = ""
row_array = []
count = 0
test_hash = {}
test_number = []
lot_id = ''
job_name = ''
temperature_global = ''
end_row = False



#Get headers
for record in root.iter():
	if(record.tag == 'Ptr'):
		test_record = record.get('TEST_TXT')
		if(test_record not in headers_arranged):
			headers_arranged.append(test_record)
		if(test_record in headers_arranged):
			break	



#Parse records
for record in root.iter():
	if(record.tag == 'Ptr'):
		test_record = record.get('TEST_TXT')
		test_result = record.get('RESULT')
		test_num = record.get('TEST_NUM')
		key = test_num + test_record

		test_hash.setdefault(test_record, []).append(test_result)
		if(test_record not in headers_arranged):
			headers_arranged.append(test_record)

	if(record.tag == 'Prr'):
		x_coord = record.get('X_COORD')
		test_hash.setdefault('X', []).append(x_coord)
		y_coord = record.get('Y_COORD')
		test_hash.setdefault('Y', []).append(y_coord)
		test_time = record.get('TEST_T')
		test_hash.setdefault('Elapsed Time', []).append(test_time)
	if(record.tag == 'Mir'):
		lot_id = record.get('LOT_ID')
		test_hash.setdefault('LOT_ID', []).append(lot_id)
		job_name = record.get('JOB_NAM')
		test_hash.setdefault('JOB_NAM', []).append(job_name)
		temperature = record.get('TST_TEMP')
		temperature_global = temperature
		test_hash.setdefault('Temperature', []).append(temperature)



#Prompt for exporting file.
sys.stdout.write('Exporting CSV file...')



#Populate the rest of arrays that have only one value
for x in range(len(test_hash[headers_arranged[20]])):
	test_hash.setdefault('LOT_ID', []).append(lot_id)
	test_hash.setdefault('JOB_NAM', []).append(job_name)
	test_hash.setdefault('Temperature', []).append(temperature_global)


#Convert/Transpose to dataframe
df = pd.DataFrame.from_dict(test_hash,orient='index')
transposed = df.transpose()
transposed_sorted = transposed.reindex(columns=headers_arranged)
transposed_sorted.to_csv(output_file, sep=',')

#Prompt on job completion
print 'File generated:',sys.argv[2]






