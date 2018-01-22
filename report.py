import numpy as np
import sys

the_date = sys.argv[1]
input_file = the_date +".log"
mymap = {}
mymap2 = {}


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
        mymap[timestamp] = line[2]
        
for v in mymap.iteritems():
    if v[1] in mymap2:
        mymap2[v[1]] = mymap2[v[1]]+1
    else:
        mymap2[v[1]] = 1
        
        
print("report for the date: " + the_date) 
total_seconds = 0
for key, value in sorted(mymap2.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    total_seconds = total_seconds + value 
    m, s = divmod(value, 60)
    h, m = divmod(m, 60)
    print "%s: %02d:%02d:%02d" % (key, h, m, s)

m, s = divmod(total_seconds, 60)
h, m = divmod(m, 60)

print "total of: %02d:%02d:%02d" % (h, m, s)

