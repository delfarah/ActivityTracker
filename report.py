import numpy as np
import sys
import math
<<<<<<< HEAD
import matplotlib.pyplot as plt

=======
>>>>>>> b2caf0d5711e7b75729fca57193b2bb8dbc3f3b1

IDLE_THRESHOLD = 60
MINUS_INFINITY = -10000000

the_date = sys.argv[1]
input_file = the_date +".log"
mymap = {}
mymap2 = {}

prev_timestamp = MINUS_INFINITY
prev_line2 = ''

timestep_start = MINUS_INFINITY

with open(input_file) as fp:
    while True:
    #for i in range(100):
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
total_up = timestamp - timestep_start
        
for v in mymap.iteritems():
    if v[1] in mymap2:
        mymap2[v[1]] = mymap2[v[1]]+1
    else:
        mymap2[v[1]] = 1
        
        
objects = list()
performance = list()
print("report for the date: " + the_date) 
total_seconds = 0
for key, value in sorted(mymap2.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    total_seconds = total_seconds + value 
    m, s = divmod(value, 60)
    h, m = divmod(m, 60)
    print "%s: %02d:%02d:%02d" % (key, h, m, s)
    if value > 60:
        objects.append(key)
        performance.append(value)

m, s = divmod(total_seconds, 60) #only show apps that were used more than 1 minute
h, m = divmod(m, 60)
print "total of: %02d:%02d:%02d" % (h, m, s)

m, s = divmod(total_up, 60)
h, m = divmod(m, 60)
print "total up time: %02d:%02d:%02d" % (h, m, s)

<<<<<<< HEAD


y_pos = np.arange(len(objects))
plt.bar(y_pos, performance, align='center', alpha=0.5)

plt.xticks(y_pos, objects, rotation=45)
plt.title('Report for: ' + the_date)
plt.ylabel('Usage (seconds)')

plt.show()
=======
>>>>>>> b2caf0d5711e7b75729fca57193b2bb8dbc3f3b1
