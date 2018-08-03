#!/usr/bin/Python
#Usage: Python find_limits.py <xml_output_from_pystdf>
#Script to find testing limits directly from STDF file xml output from pystdf
import xml.etree.ElementTree as ET
import csv
import sys
import re
import pandas as pd

input_file = sys.argv[1]
tree = ET.parse(input_file)
root = tree.getroot();
limits_dictionary = {}
limits_array = []
count = 0
for record in root.iter():
	if(record.tag == 'Ptr'):
		test_name = record.attrib['TEST_TXT']
		if (test_name not in limits_dictionary):
			hi_limit = record.attrib['HI_LIMIT']
			low_limit = record.attrib['LO_LIMIT']
			unit = record.attrib['UNITS']
			limits_dictionary[test_name] = [low_limit,hi_limit,unit]
			limits_array.append([test_name,low_limit,hi_limit,unit])

		else:
			break
		count = count + 1


sys.stdout.write('Test Name')
sys.stdout.write(',')
sys.stdout.write('LO_LIMIT')
sys.stdout.write(',')
sys.stdout.write('HI_LIMIT')
sys.stdout.write(',')
sys.stdout.write('UNITS')
sys.stdout.write('\n')

for x in range(len(limits_array)):
	sys.stdout.write(limits_array[x][0])
	sys.stdout.write(',')
	sys.stdout.write(limits_array[x][1])
	sys.stdout.write(',')
	sys.stdout.write(limits_array[x][2])
	sys.stdout.write(',')
	sys.stdout.write(limits_array[x][3])
	sys.stdout.write('\n')


