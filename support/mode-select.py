
# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.
# Please see the LICENSE file that should have been included as part of this package.

import time
time.sleep(1)

#     import cv2
import sys
import os

from subprocess import check_call, call, run
import RPi.GPIO as GPIO

# For run a start-up and shutdown with button
from gpiozero import LED, Button
#     from subprocess import check_call
#     from signal import pause

was_held = False  # is for GPIOzero

ex = False
stop_check_mode = False
stop_reboot = False
stop_plus = False


# Subtract len of file name and / to get containing directory, and - 8 more for "/support"
rc_dir = os.path.abspath(__file__)
rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 9]


# # For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
# path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
# path_usb = path_usb.decode("utf-8").splitlines()[0]
# path_usb = "/media/pi" + "/" + path_usb
# # This should create a path to any removable storage ----------------------------------

b = open(rc_dir + "/support/comm2.txt", "r")
back_to = b.read()
b.close()


#     def exi():     # works here and closes threads fast with gray btn, but except triggers
# #         GPIO.cleanup()
#         print("EXITING with exi in mode select--")
#         time.sleep(2)
#         # Takes 10s to exit after sys.exit called_sel GPIOzero trying to close thread
#         sys.exit()

def shutdown():           # has zombie thread issue
    global stop_reboot
    stop_reboot = True

    global ex
    ex = True

    run(['python3', rc_dir + '/support/shutdown.py'])


def reboot():
    global stop_reboot    # does not have zombie thread issue
    if stop_reboot == False:

        global ex
        ex = True
        run(['python3', rc_dir + '/support/reboot.py'])

def reboot_gray():
    global stop_reboot
    global stop_plus
    stop_plus = True
    time.sleep(0.1)
    if stop_reboot == False:
        global ex
        ex = True
        run(['python3', rc_dir + '/support/reboot.py'])

def mode_plus():
    global stop_plus
    global path_usb
    if stop_plus == False:
        global count
        f = open(rc_dir + "/support/RC_config.txt", "r")
        prog = f.read().splitlines()   # gets ride of the \n at end of each element
#         print(prog)
        for idx, i in enumerate(prog):
            if "mode =" in i:
                m = prog[idx].split()
                m = int(m[-1]) + 1
                if m > count:    # Cycle through this many mode files, number of mode files are counted
                    m = 1
                prog[idx] = "mode =" + " " + str(m)

        f.close()

        f = open(rc_dir + "/support/RC_config.txt", "w")
        f.truncate(0)
        for i in prog:
            f.write(i + "\n")
        f.close()

#         print("mode updated ", m)
        for i in range(m):
            led_sel.on()
            time.sleep(1)
            led_sel.off()
            time.sleep(1)

# replacing reboot_gray with this, don't need to reboot.
def to_selected_mode():
    global path_usb, back_to
    
    
    f = open(rc_dir + "/support/RC_config.txt", "r")
    prog = f.read().splitlines()   # gets ride of the \n at end of each element
    f.close()
    
    b = open(rc_dir + "/support/comm2.txt", "w")
    b.write("sel")
    b.close()

#     print(prog)
    for idx, i in enumerate(prog):
        if "mode =" in i:
            m = prog[idx].split()
            m = int(m[-1])

    global stop_reboot
    global stop_plus
    stop_plus = True
    time.sleep(0.1)
    if stop_reboot == False:
        et = 0.05
        for i in range(10):
            led_sel.on()
            time.sleep(et)
            led_sel.off()
            time.sleep(et)
            et += et * 0.2
        global ex
        ex = True
        
        if back_to != "dis":
#             print("launch file in selectm-mode.py------------")
            # Takes 10s to exit after sys.exit called GPIOzero trying to close thread
            run(['python3', f'{rc_dir}/modes/mode{m}.py'])
        else:
            run(['python3', f'{rc_dir}/support/disable.py'])


modes = run(["ls", rc_dir + "/modes"], capture_output=True).stdout

modes = modes.decode("utf-8").splitlines()

count = 0
for i in modes:
    if  "mode" in i.lower() and ".py" in i.lower():
#         print(i)
        count += 1

led_sel = LED(26)

red_btn = Button(17, hold_time=2)
red_btn.when_held = shutdown
red_btn.when_released = reboot

gray_btn = Button(27, hold_time=2)
gray_btn.when_held = to_selected_mode
gray_btn.when_released = mode_plus

et = 0.3
for i in range(10):
    led_sel.on()
    time.sleep(et)
    led_sel.off()
    time.sleep(et)
    et -= et * 0.2

while True:
#         global ex   no
    time.sleep(0.1)
    if ex == True:
        break

GPIO.cleanup()   # try see if stops zombie
# .close() on zero threads does not stop zombies
time.sleep(0.5)
# print("OK exiting select mode NOW")
sys.exit()


