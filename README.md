# ActivityTracker
A simple program in C++ that can monitor your activity


The plan

1. get the window which the focus is on right now.
2. Get mouse and keyboard events if it changes the active window you may need to reset/set the timers.
3. if keyboard and mouse both go idle. Then stop tracking until you recieve an event

The process will work in the background forever. It writes the logs in file.
A separate program will be used to display the results.
