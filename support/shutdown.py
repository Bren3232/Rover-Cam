

from subprocess import run
import time

# print("in shutdown file - shutting down in 11 sec")
# time.sleep(1)

time.sleep(11)

run(['sudo', 'shutdown', 'now'])


