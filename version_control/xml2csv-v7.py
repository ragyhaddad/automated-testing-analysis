#Author: Ragy Haddad
#Pipeline -> xml stdf to csv
#Takes in xml file from pystdf and converts it to csv

import xml.etree.ElementTree as ET
import csv
import sys
import re
import pandas as pd
import os
import decimal


#---------------------------------------------------#
#Usage check
if(len(sys.argv) < 3):
	print('Usage: python xml2csv-v5.py <input.xml> <output.csv>')
	sys.exit(1)

print('Importing file...')

hash_data = {}
#Import/parse xml
tree = ET.parse(sys.argv[1])
root = tree.getroot()
temp_filename = sys.argv[2] + 'temp.csv'
#Open a file for writing
output_file = open(sys.argv[2], 'w')
temp_file = open('temp.csv', 'w')


headers_arranged = ['Lot Number','Job Name','Temperature','X','Y','Elapsed Time']
columnNumber = 0
final_headers = 0

def createDevice(site_num,device_count):
    array = []
    array.append(device_count,site_num)
    return array



#Lot id, lot number,Part Id, X , Y, Time
#  
header_array = []
device_count = 0
part_id = 0
parallel_count = 0
pir_count = 0
lot_id = ''
part_type = ''
max_prr = 0
global_x = 0
global_y = 0
global_time = 0


#Install a new device
def installArray(global_part_id, site_number):
    key = str(global_part_id)+ '-' + str(site_number)
    newarray = []
    hash_data[str(key)] = newarray
    hash_data.setdefault(key,[]).append(lot_id)
    hash_data.setdefault(key,[]).append(part_type)
    hash_data.setdefault(key,[]).append(global_part_id)
    hash_data.setdefault(key,[]).append(global_x)
    hash_data.setdefault(key,[]).append(global_y)
    hash_data.setdefault(key,[]).append(global_time)
#Parse XML output from pystdf
for record in root.iter():
    if(record.tag == 'Mir'):
        lot_id = record.attrib['LOT_ID']
        part_type = record.attrib['PART_TYP']
    if(record.tag == 'Prr'):
        device_count = device_count + 1
        site_num = record.get('SITE_NUM')
        max_prr = site_num
        part_id = record.attrib['PART_ID']
        installArray(part_id,site_num)
        global_x = record.get('X_COORD')
        global_y = record.get('Y_COORD')
        global_time = record.get('TEST_T')
        parallel_count = parallel_count + 1 #stores the number of devices in parallel        
    if(record.tag == 'Ptr'):
        site_number = record.attrib['SITE_NUM']
        test_name = record.get("TEST_TXT")
        if(test_name not in header_array):
            header_array.append(test_name)
        index = part_id
        site_num = record.get('SITE_NUM')  
        if(parallel_count > 1):
            index = int(part_id) - (parallel_count - (int(site_num) + 1))  
        regen_key =str(index) + '-' + str(site_num)
        test_result = record.attrib['RESULT']
        result_formatted = '{:.15}'.format(float(test_result))
       
        if(regen_key not in hash_data):
            installArray(index,site_num)
        # hash_data.setdefault(regen_key,[]).append(test_result)
        hash_data[regen_key].append(result_formatted)


        
    if(record.tag == 'Eps'):
        parallel_count = 0
        pir_count = 0


#---------------------------------------------------

#Append header names to hash
all_headers = ['Lot Id', 'Lot Number', 'Part Id', 'X', 'Y','Time'] + header_array
hash_data['-1-0'] = all_headers
        


#Convert/Transpose to dataframe
df = pd.DataFrame.from_dict(hash_data,orient='index')

#Drop devices that did not enter test
df = df.ix[~(df[6].isnull())]
#Write dataframe to csv and remove temp file
df.to_csv(temp_file, sep=',')
command = 'sort -k 1 -n temp.csv > ' + sys.argv[2]
os.system(command)
os.system('rm temp.csv')

















