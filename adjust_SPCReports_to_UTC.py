import numpy as np
from datetime import datetime, timedelta
import os
import csv

##########################################################################################
#
# This script is intended to change the CSV archived SPC official storm events
# from CST time to UTC time. Check the filepath and fname variables to match your
# personal system and file paths. The SPC archived CSV files can be downloaded
# from this webpage: spc.noaa.gov/wcm/#data. Script was written to be run within
# anaconda 4.9.2. Make sure you have properly downloaded the packages above.
#
# Authored by Joseph Patton (@JosephPattonWx on twitter). Last modified on 26 March 2021.
#
##########################################################################################

filepath = '/Users/bjig2/Documents/GIS/Projects/SPC_Severe/'
fname = '{}1955-2019_wind.csv/1955-2019_wind.csv'.format(filepath)
newfname = '1955-2019_wind_UTC.csv'
newfile_towrite = csv.writer(open(newfname, 'w',newline=''))
with open(fname) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			print(f'Column names are {",".join(row)}')
			line_count += 1
			newfile_towrite.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
					row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],
					row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28]])
		else:
			#if line_count < 10:
				storm_date = row[4]
				storm_time = row[5]
				storm_datetime = storm_date + ' ' + storm_time
				print(f'\tThe storm_datetime is {storm_datetime}.')
				old_datetime = datetime.strptime(storm_datetime, '%Y-%m-%d %H:%M:%S')
				#old_datetime = datetime.strptime(storm_datetime, '%m/%d/%Y %H:%M:%S')
				print(f'\tThe date is {storm_date} and the time is {storm_time}.')
				#print(f'\tThe date and time is {old_datetime}.')
				new_datetime = old_datetime + timedelta(hours=6)
				#print(f'\tThe new date and time is {new_datetime}.')
				new_date = new_datetime.strftime("%m/%d/%Y")
				new_time = new_datetime.strftime("%H:%M:%S")
				new_year = new_datetime.strftime("%Y")
				new_month = new_datetime.strftime("%m")
				new_day = new_datetime.strftime("%d")
				print(f'\tThe new date and time is {new_date} {new_time}.')
				#writer = csv.writer(newfname)
				#print(f'\trow[0] represents {row[0]}.')
				newfile_towrite.writerow([row[0],new_year,new_month,new_day,new_date,new_time,row[6],row[7],row[8],row[9],
					row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],
					row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28]])
				line_count += 1
	print(f'Processed {line_count} lines.')



