import subprocess
import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

while(True):
    output1, _ = subprocess.Popen("xdotool getwindowfocus".split(), stdout=subprocess.PIPE).communicate()
    output2, _ = subprocess.Popen(("xdotool getwindowpid "+output1).split(), stdout=subprocess.PIPE).communicate()
    output3, _ = subprocess.Popen(("cat /proc/"+output2[:-1]+"/comm").split(), stdout=subprocess.PIPE).communicate()
    time.sleep(1)
    logger.info(output3[:-1])
#    print(output3)
