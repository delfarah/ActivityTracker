# ActivityTracker
A simple program that can monitor your activity


The plan

1. get the window which the focus is on right now.
2. Get mouse and keyboard events if it changes the active window you may need to reset/set the timers.
3. if keyboard and mouse both go idle. Then stop tracking until you recieve an event

The process will work in the background forever. It writes the logs in file.
A separate program will be used to display the results.


Notes:
cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm can do the job

for keyboard: https://www.tecmint.com/how-to-monitor-keyboard-keystrokes-using-logkeys-in-linux/
for mouse: xdotool can handle this.
Keyboard gives a log file which works well
for mouse I check pointer position every 200ms and if see a change then I am active

Combine these two logs to initiate the report

Apps to handle for now:
nautalius
gnome-terminal
terminator
chrome (+title of window)
desktop

