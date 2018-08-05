'''
1. Download excel file from radar
2. Extract hostnames from the file
3. ssh into each host and get the timestamp of the last successful ansible run
4. Compare the timestamp with current time
5. Raise alert if difference exceeds 120 minutes.

'''


import xlrd
import os
import time


# Open the excel file

loc = ('/home/seshadri/scripts/python/alerts.xlsx')

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# Record current time

current_time = int(time.time())

# Delete if the temp file exists

try:
    os.remove('/tmp/data.txt')
except:
    pass

# Initialize an empty list of hosts

host_list = []

# Create a file in append mode

data_file = open('/tmp/data.txt', 'a+')

# print (sheet.nrows)

# Initialize the number of rows in the sheet that needs to be parsed
# The first row is a heading and should be discarded, so we start from 1

start = 1
stop = sheet.nrows

for i in range(start,stop):
    data_file.write(sheet.cell_value(i,0).split()[-1] + '\n')
    
    
data_file.close()

# Run ongroup on each host and get the timestamp of the last successful ansible run