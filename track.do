xinput test-xi2 --root > tmp_log.txt &

activity_DATE=`date +%Y-%m-%d`
old_count=0
the_limit=1000

while true
do
     sleep 1
     new_count=`cat tmp_log.txt | wc -l`
     
     if [ "$new_count" != "$old_count" ]; then
        the_app=`cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm`
        the_date=`date '+%Y-%m-%d %H:%M:%S'`
        str=$the_date' '$the_app
        echo $str >> $activity_DATE.log
        old_count=$new_count
     fi
     if [ "$new_count" -gt "$the_limit" ]; then
        truncate -s0 tmp_log.txt
     fi
done
