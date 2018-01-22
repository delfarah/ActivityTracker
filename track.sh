#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
export DISPLAY=:0.0

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
xinput test-xi2 --root > tmp.log &

old_count=0
the_limit=1000

while true
do
     sleep 1
     new_count=`cat tmp.log | wc -l`
     
     if [ "$new_count" != "$old_count" ]; then
        the_app=`cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm`
        the_date=`date '+%Y-%m-%d %H:%M:%S'`
        activity_DATE=`date +%Y-%m-%d`
        win_title=`wmctrl -lp | grep $(xprop -root | grep _NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/')`
        str=$the_date' '$the_app' '$win_title
        echo $str >> $activity_DATE.log
        old_count=$new_count
     fi
     if [ "$new_count" -gt "$the_limit" ]; then
        truncate -s0 tmp.log
     fi
done
