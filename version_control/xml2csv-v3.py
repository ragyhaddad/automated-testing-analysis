#Author: Ragy Haddad
#Pipeline -> xml stdf to csv
#Takes in xml file from pystdf and converts it to csv

import xml.etree.ElementTree as ET
import csv
import sys
import re
import pandas as pd


# print 'Importing file',sys.argv[1]

#---------------------------------------------------#

#Import/parse xml
tree = ET.parse(sys.argv[1])
root = tree.getroot()
#Open a file for writing
output_file = open(sys.argv[2], 'w')
#Create the csv writer object
headers_arranged = ['LOT_ID','JOB_NAM','Temperature','X','Y','Elapsed Time']
columnNumber = 0



#---------------------------------------------------#

#Variables
count = 0
header_array = []
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
dictionary_dev_test = {}
site_num_unpair = 0
#---------------------------------------------------#

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
		site_num_unpair = record.get('SITE_NUM')
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
		##Parse Headers
		record_name = record.get('TEST_TXT')
		if(record_name not in header_array):
			header_array.append(record_name)

		##Case 1 - One device Ptr
		if(two_devices == False):
			test_site_unpair = record.get('SITE_NUM')
			if(test_site_unpair == site_num_unpair):
				record_result = record.get('RESULT')
				array_device.append(record_result)
				test_counter = test_counter + 1
		##Case 2 - Two Device Ptr
		if(two_devices == True):
			site_num = record.get('SITE_NUM')
			if(site_num == '0'):
				test_result_1 = record.get('RESULT')
				array_device_1.append(test_result_1)
				length_1 = length_1 + 1
			if(site_num == '1'):
				test_result_2 = record.get('RESULT')
				array_device_2.append(test_result_2)
				length_2 = length_2 + 1
	if(record.tag == 'Eps'): #End of Record
		two_device_switch = 0
		if(two_devices == True):
			length_1 = 0
			length_2 = 0
			##Append the two arrays to hash
			hash_data.setdefault(count_1,[]).append(array_device_1)
			hash_data.setdefault(count_2,[]).append(array_device_2)
			#Switch Off the switch mode
			two_devices = False	
			count_1 = 0
			count_2 = 0
		else:
			hash_data.setdefault(device_count, []).append(array_device)
			array_device = []
		
		
#---------------------------------------------------#

count_rows = 0
for key in hash_data:
	if(count_rows == 0):
		count_rows = count_rows + 1
		line = ",".join(header_array)
		output_file.write(line)
		output_file.write('\n')
	else:
		line = ",".join(hash_data[key][0])
		count_rows = count_rows + 1
		output_file.write(line)
		output_file.write('\n')













