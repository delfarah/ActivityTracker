import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from colorama import Fore
from datetime import datetime
from datetime import timedelta
import os
import pickle
import getpass

IDLE_THRESHOLD = 60 #in seconds
MINUS_INFINITY = -10000000


current_date = datetime(2018, 1, 1) #track from 2018 to today


days_report_file_name = getpass.getuser() + '.pickle'

if os.path.isfile(days_report_file_name):
    with open(days_report_file_name, 'rb') as handle:
        date_to_times = pickle.load(handle)   # date -> [productive, total desk]
else:
    date_to_times = {}

while current_date < datetime.today() + timedelta(days=-1):
    current_date += timedelta(days=1)

    current_date_string = current_date.strftime('%Y-%m-%d')
    
    if current_date_string in date_to_times and current_date_string != datetime.today().strftime('%Y-%m-%d'): #always assess today because its being updated at the moment
        continue

    input_file = current_date_string + '.log'
    mymap = {}
    mymap2 = {}
    
    prev_timestamp = MINUS_INFINITY
    prev_line2 = ''
    
    timestep_start = MINUS_INFINITY
    print(input_file)
    if not os.path.isfile(input_file):
        date_to_times[current_date_string] = [0, 0]
        continue

    with open(input_file) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
    
            line = line.replace("\n", "")
            line = line.split(" ",3)
            if(len(line) < 3):
                continue
            timestamp = line[1].split(":")
            timestamp = 3600*int(timestamp[0]) + 60*int(timestamp[1]) + int(timestamp[2])
            if timestep_start == MINUS_INFINITY:
                timestep_start = timestamp
                
            if prev_timestamp + IDLE_THRESHOLD > timestamp:
                while prev_timestamp < timestamp:
                    prev_timestamp += 1
                    mymap[prev_timestamp] = prev_line2
                    
            prev_timestamp = timestamp
            prev_line2 = line[2]
            
            mymap[timestamp] = line[2]
    total_office = timestamp - timestep_start
            
    for v in mymap.iteritems():
        if v[1] in mymap2:
            mymap2[v[1]] = mymap2[v[1]]+1
        else:
            mymap2[v[1]] = 1
            
            
    objects = list()
    performance = list()
    total_desk = 0
    for key, value in sorted(mymap2.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        total_desk = total_desk + value 
        m, s = divmod(value, 60)
        h, m = divmod(m, 60)
        if value > 60:
            objects.append(key)
            performance.append(value)
    

    
    
    
    #total_productive_time = total_desk-performance[objects.index('chrome')]-performance[objects.index('Telegram')]
    total_productive_time = total_desk
    for activity in ('chrome' , 'Telegram'): # add here any source of desctraction, still does not differenciate between chrome tabs. Do your productive work on Firefox :D
        if activity in objects:
            total_productive_time = total_productive_time - performance[objects.index(activity)]
    
    date_to_times[current_date_string] = [total_productive_time, total_desk]

with open(days_report_file_name, 'wb') as handle:
    pickle.dump(date_to_times, handle, protocol=pickle.HIGHEST_PROTOCOL)

os.system("scp " + days_report_file_name + " delfarah@pnl20.cse.ohio-state.edu:/home/delfarah/tracker")
os.system("scp " + " delfarah@pnl20.cse.ohio-state.edu:/home/delfarah/tracker/* .")


#load mgn and mighty pickles, add all the numbers one by one, then show results!
