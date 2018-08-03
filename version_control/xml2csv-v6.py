#Author: Ragy Haddad
#Pipeline -> xml stdf to csv
#Takes in xml file from pystdf and converts it to csv

import xml.etree.ElementTree as ET
import csv
import sys
import re
import pandas as pd




#---------------------------------------------------#
#Usage check
if(len(sys.argv) < 3):
	print('Usage: python xml2csv-v5.py <input.xml> <output.csv>')
	sys.exit(1)

print('Importing file...')


#Import/parse xml
tree = ET.parse(sys.argv[1])
root = tree.getroot()

#Open a file for writing
output_file = open(sys.argv[2], 'w')


headers_arranged = ['Lot Number','Job Name','Temperature','X','Y','Elapsed Time']
columnNumber = 0



#---------------------------------------------------#

#Variables
count = 0
header_array = []
test_hash = {}
test_number = []
lot_id = ''
job_name = ''
part_type = ''
temperature_global = ''
hash_data = {}
array_device = []
test_counter = 0
track_device = True
two_devices = False
two_device_switch = 0 #switch to one when finding to PRR in a row
length_1 = 0
length_2 = 0
device_count = 0
dictionary_dev_test = {}
site_num_unpair = 0 #Handle Unpaired Case
info_array = []
#---------------------------------------------------#

headers_info = ["Part Type","Lot Id","x","y","Site Num","Test Time"]
#Parse XML output from pystdf
for record in root.iter():
	#Parametric test record
	test_time = ''
	x = 0
	y = 0
	if(record.tag == 'Mir'):
		part_type = record.attrib['PART_TYP']
		lot_id = record.attrib['LOT_ID']
	if(record.tag == 'Prr'):
		info_array = []
		device_count = device_count + 1
		test_counter = 0
		track_device = True
		array_device = []
		test_counter = 0
		two_device_code = record.get('SITE_NUM')
		two_devices = False
		site_num_unpair = record.get('SITE_NUM')
		x = record.attrib['X_COORD']
		y = record.attrib['Y_COORD']
		test_time = record.get('TEST_T')
		info_array = [part_type,lot_id,x,y,site_num_unpair,test_time]
		##Two device mode
		if(two_device_code == '0'):
			x1 = record.attrib['X_COORD']
			y1 = record.attrib['Y_COORD']
			two_devices = False
			count_1 = device_count
			two_device_switch = 1
			info_array_1 = [part_type,lot_id,x1,y1,two_device_code,test_time]
		if(two_device_code == '1'):
			two_devices = True
			x2 = record.attrib['X_COORD']
			y2 = record.attrib['Y_COORD']
			info_array_2 = [part_type,lot_id,x2,y2,two_device_code,test_time]
			array_device_1 = []
			array_device_2 = []
			count_2 = count_1 + 1

			if(two_device_switch !=1):
				two_devices = False	

	#Parametric Test
	if(record.tag == 'Ptr'):
		##Parse Headers
		record_name = record.get('TEST_TXT')
		if(record_name not in header_array):
			header_array.append(record_name)

		##Case 1 - One device Ptr
		if(two_devices == False):
			test_site_unpair = record.get('SITE_NUM')
			if(test_site_unpair == site_num_unpair):
				record_result = (record.attrib['RESULT'])
				array_device.append(record_result)
				test_counter = test_counter + 1
		##Case 2 - Two Device Ptr
		if(two_devices == True):
			site_num = record.get('SITE_NUM')
			if(site_num == '0'):
				# test_result_1 = float(record.get('RESULT'))
				test_result_1 = (record.attrib['RESULT'])
				array_device_1.append(test_result_1)
				length_1 = length_1 + 1
			if(site_num == '1'):
				# test_result_2 = float(record.get('RESULT'))
				test_result_2 = (record.attrib['RESULT'])
				array_device_2.append(test_result_2)
				length_2 = length_2 + 1

	if(record.tag == 'Eps'): #End of Record
		two_device_switch = 0
		if(two_devices == True):
			length_1 = 0
			length_2 = 0
			hash_data[count_1] = info_array_1 + array_device_1 #added info
			hash_data[count_2] = info_array_2 + array_device_2
			#Switch Off the switch mode
			two_devices = False	
			count_1 = 0
			count_2 = 0
		else:
			hash_data[device_count] = info_array + array_device
			array_device = []
		
		
#---------------------------------------------------
final_headers = headers_info + header_array
hash_data[0] = final_headers

#Convert/Transpose to dataframe
count_rows = 0
df = pd.DataFrame.from_dict(hash_data,orient='index')
# df.style.set_precision(20)
df.dropna(axis=0,how='all',inplace=True)
df.to_csv(output_file, sep=',')

















