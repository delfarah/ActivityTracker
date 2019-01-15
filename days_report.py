#!/usr/bin/env python

import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import matplotlib
from colorama import Fore
from datetime import datetime
from datetime import timedelta
import os
import pickle
import getpass
import pylab
import calendar

IDLE_THRESHOLD = 60 #in seconds
MINUS_INFINITY = -10000000

checked_listory_file = 'checked_history.pickle'
if not os.path.isfile(checked_listory_file):
    last_checked = {}
    last_checked[datetime.today().strftime('%Y-%m-%d')] = 0
    with open(checked_listory_file, 'wb') as handle:
        pickle.dump(last_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(checked_listory_file, 'rb') as handle:
    last_checked = pickle.load(handle)   # date -> [productive, total desk]
last_checked[datetime.today().strftime('%Y-%m-%d')] += 1
with open(checked_listory_file, 'wb') as handle:
    pickle.dump(last_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

if last_checked[datetime.today().strftime('%Y-%m-%d')] > 2:
    print('Already exceeded maximum allowd times to check the tracker')
    exit(0)


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

os.system("scp " + days_report_file_name + " osu8420@owens.osc.edu:/users/PAS0774/osu8420/tracker")
os.system("scp " + " osu8420@owens.osc.edu:/users/PAS0774/osu8420/tracker/* .")



with open('mighty.pickle', 'rb') as handle:
    date_to_times1 = pickle.load(handle)   # date -> [productive, total desk]
with open('delfarah.1.pickle', 'rb') as handle:
    date_to_times2 = pickle.load(handle)   # date -> [productive, total desk]

date_to_times = {}

for v in date_to_times1.iteritems():
    date_to_times[v[0]] =  [sum(x) for x in zip(date_to_times1[v[0]], date_to_times2[v[0]])]



#Print from 2019-01-01 to today
worked_time = list()
all_desk_time = list()
titles = list()
start_date = datetime(2019, 1, 1) #track from 2018 to today
#end_date = datetime(2018, 12, 30)
end_date = datetime.today()

current_date = start_date
while current_date < end_date:
    current_date_string = current_date.strftime('%Y-%m-%d')
    current_date_string_weekday = calendar.day_name[current_date.weekday()] 

#    if current_date_string in date_to_times:
#        print( current_date_string + ' ' + str(date_to_times[current_date_string]))

    all_desk_time += (date_to_times[current_date_string][1]/3600.,)
    worked_time += (date_to_times[current_date_string][0]/3600.,)
    titles += (current_date_string[5:]+' '+current_date_string_weekday,)


    current_date += timedelta(days=1)

from matplotlib.pyplot import figure
figure(figsize=(len(worked_time)/2, 6))


font = {'size' : 9}
matplotlib.rc('font', **font)

ind = np.arange(len(worked_time))    # the x locations for the groups
width = 0.80       # the width of the bars: can also be len(x) sequence

plt.grid(color='black', linestyle='dotted', linewidth=0.5, axis='y', zorder=0)

p1 = plt.bar(ind, all_desk_time, width, color='tomato', zorder=3)
p2 = plt.bar(ind, worked_time, width, color='limegreen', zorder=3)

plt.ylabel('Hours')
plt.xticks(ind, titles)
plt.xticks(rotation=90)
plt.yticks(np.arange(0, 12, 1))
plt.legend((p1[0], p2[0]), ('Distraction', 'Productive'))


for i in range(len(worked_time)):
    height = p1[i].get_height()
    if p1[i].get_height() == 0:
    	percent_value = 0
    else: 
    	percent_value = float(100 *p2[i].get_height() / p1[i].get_height())
    plt.text(p1[i].get_x() + p1[i].get_width()/2., 1.05*height, '%%%.1f' % percent_value , ha='center', va='bottom', rotation=90,)

plt.subplots_adjust(top=0.9, bottom=0.3)
pylab.savefig('report.pdf')


os.system('gnome-open report.pdf')
