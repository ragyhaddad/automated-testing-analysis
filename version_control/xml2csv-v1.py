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
hash_data = {}
array_all = []
array_device = []
test_counter = 0
track_device = True
two_devices = False
two_device_switch = 0 #switch to one when finding to PRR in a row
length_1 = 0
length_2 = 0
device_count = 0









#Parse XML output from pystdf
for record in root.iter():
	#If one record
	if(record.tag == 'Prr'):
		device_count = device_count + 1
		test_counter = 0
		track_device = True
		array_device = []
		test_counter = 0
		two_device_code = record.get('SITE_NUM')
		two_devices =False
		
		##Two device mode
		if(two_device_code == '0'):
			two_devices = False
			count_1 = device_count
			two_device_switch = 1
		if(two_device_code == '1'):
			two_devices = True
			array_device_1 = []
			array_device_2 = []
			count_2 = count_1 + 1
			if(two_device_switch !=1):
				two_devices = False	

	if(record.tag == 'Ptr'):
		record_name = record.get('TEST_TXT')
		if(test_record not in headers_arranged):
			headers_arranged.append(test_record)
		if(two_devices == False):
			record_result = record.get('RESULT')
			array_device.append(record_result)
			test_counter = test_counter + 1
		if(two_devices == True):
			site_num = record.get('SITE_NUM')
			if(site_num == '0'):
				test_result = record.get('RESULT')
				array_device_1.append(test_result)
				length_1 = length_1 + 1
			if(site_num == '1'):
				test_result = record.get('RESULT')
				array_device_2.append(test_result)
				length_1 = length_2 + 1

	if(record.tag == 'Eps'): #End of Record
		two_device_switch = 0
		if(two_devices == True):
			if(len(array_device_1) < 58):
				while length_1 < 58:
					array_device_1.append('NA')
					length_1 = length_1 + 1
			if(len(array_device_2) < 58):
				while length_2 < 58:
					array_device_2.append('NA')
					length_2 = length_2 + 1
			##Append the two arrays to hash
			hash_data.setdefault(count_1,[]).append(array_device_1)
			hash_data.setdefault(count_2,[]).append(array_device_2)
			#Switch Off the switch mode
			two_devices = False	
		else:
			if(len(array_device) < 58):
				while test_counter < 58: #Handle Test Failures
					array_device.append('NA')
					test_counter = test_counter + 1
			hash_data.setdefault(device_count, []).append(array_device)
		
		

print(device_count)
print(hash_data[7800])
print(len(hash_data))

print(hash_data[193])



#Prompt for exporting file.
# sys.stdout.write('Exporting CSV file...')



# #Populate the rest of arrays that have only one value
# for x in range(len(test_hash[headers_arranged[20]])):
# 	test_hash.setdefault('LOT_ID', []).append(lot_id)
# 	test_hash.setdefault('JOB_NAM', []).append(job_name)
# 	test_hash.setdefault('Temperature', []).append(temperature_global)


# #Convert/Transpose to dataframe
# df = pd.DataFrame.from_dict(test_hash,orient='index')
# transposed = df.transpose()
# transposed_sorted = transposed.reindex(columns=headers_arranged)
# transposed_sorted.to_csv(output_file, sep=',')

# #Prompt on job completion
# print 'File generated:',sys.argv[2]






