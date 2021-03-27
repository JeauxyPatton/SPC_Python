import numpy as np
from datetime import datetime, timedelta
import os
import csv

################################################################################
#
# Set outbreak_day to the correct day in the format YYYYMMDD
# and this script will generate the official WIND reports from
# 12:00:00 UTC on that day to 12:00:00 on the next day. This can be
# tailored to whatever time frame you want by adjusting begin_time
# and the input for timedelta in the variable end_datetime.
#
# Check the file paths in fname and newfname to match your system.
#
# Last modified by Joseph Patton (@JosephPattonWx on twitter) on 26 March 2021
# Only tested in anaconda 4.9.2.
#
################################################################################

outbreak_day = "20030504"
begin_time = "12:00:00"
begin_time_and_day = outbreak_day + ' ' + begin_time
begin_datetime = datetime.strptime(begin_time_and_day, '%Y%m%d %H:%M:%S')
end_datetime = begin_datetime + timedelta(hours=24)

fname = "/Users/bjig2/Documents/GIS/Projects/SPC_Severe/1955-2019_wind_UTC.csv"
newfname = "/Users/bjig2/Documents/GIS/Projects/SPC_Severe/{}/{}_wind_UTC.csv".format(outbreak_day,outbreak_day)
print(f'\tThe new CSV file is being written to {newfname}.')
newfile_towrite = csv.writer(open(newfname, 'w',newline=''))
with open(fname) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			#print(f'Column names are {",".join(row)}')
			line_count += 1
			newfile_towrite.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
					row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],
					row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28]])
		else:
				storm_date = row[4]
				storm_time = row[5]
				storm_datetime = storm_date + ' ' + storm_time
				#print(f'\tThe storm_date is {storm_date}.')
				storm_datetime = datetime.strptime(storm_datetime, '%m/%d/%Y %H:%M:%S')
				if ((storm_datetime >= begin_datetime) and (storm_datetime <= end_datetime)):
					print(f'\tThe wind report time is {storm_datetime}.')
				#writer = csv.writer(newfname)
				#print(f'\trow[0] represents {row[0]}.')
					newfile_towrite.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
						row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],
						row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28]])
					line_count += 1
	print(f'Processed {line_count} wind reports.')



