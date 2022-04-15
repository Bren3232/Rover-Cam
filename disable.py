#!/usr/bin/env python3


# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.


# This file starts when mode is disabled and relaunches the same mode, or reboots the pi
# when blue button pressed (in code sequence?)
# cpu usage, almost none

# Lock time is applied here

import time
time.sleep(1)
# sleep needed for GPIOzero btn's to work when coming out of "select"
# 15s give about 4s buffer space. But is more like 1s now bc of led flash in select
# print("============diabled.py start")

import cv2
import numpy as np
import random
import sys
from subprocess import check_call, call, run
from gpiozero import LED, Button
#     from signal import pause

was_held = False

ex = False
stop_check_mode = False
stop_reboot = False
play = False
bbp = 0
des = 0
bb_time = 0
fa_num = 0

dis_rdy = False

from threading import Thread
import RPi.GPIO as GPIO


def exi():
#         print("sys exit in some loop")
    import sys
    GPIO.cleanup()
    #ca.release()
#     print("EXITING mode2 in + 10? secs")
    time.sleep(0.1)
    # Takes 10s to exit after sys.exit called GPIOzero trying to close thread
    sys.exit()


def shutdown():           # has zombie thread issue
    global stop_reboot
    stop_reboot = True

    global ex
    ex = True

    run(['python3', '/home/pi/Desktop/Rover_Cam/shutdown.py'])
#         check_call(['sudo', 'poweroff'])  # old way


def reboot():
    global stop_reboot    # does not have zombie thread issue
    if stop_reboot == False:

        global ex
        ex = True

        run(['python3', '/home/pi/Desktop/Rover_Cam/reboot.py'])
#         check_call(['sudo', 'reboot'])  #old way


def goto_mode_select():          # has zombie thread issue
#     print("in goto_mode_select")
    global stop_check_mode
    stop_check_mode = True
    # check call another py
#     print("sys exitting going to select")
    
    b = open("/home/pi/Desktop/Rover_Cam/comm2.txt", "w")
    b.write("dis")
    b.close()

    global ex
    ex = True

    run(['python3', '/home/pi/Desktop/Rover_Cam/mode-select.py'])
    # sys exit here closes only this thread, see os._exit() but have know how to use


# def check_mode():       # zombie thread issue
#     if stop_check_mode == False:
# #             sys.exit()       # stops thread but may interfere with GPIOzero stop thead
# #         print("in check_mode")
#         # blink led number of times equal to mode number
#         global mode
#         for i in range(mode):
#             led_dis.on()
#             time.sleep(1)
#             led_dis.off()
#             time.sleep(1)


# replacing reboot_gray with this, don't need to reboot.
def to_selected_mode():
    global path_usb
    f = open(path_usb + "/RC_config.txt", "r")
    prog = f.read().splitlines()   # gets ride of the \n at end of each element
    f.close()

#     print(prog)
    for idx, i in enumerate(prog):
        if "mode =" in i:
            m = prog[idx].split()
            m = int(m[-1])

    global stop_reboot
    global stop_plus
    stop_plus = True
    global dis_rdy
    time.sleep(0.1)
    if stop_reboot == False:
        et = 0.05
        for i in range(10):
            led_dis.on()
            time.sleep(et)
            led_dis.off()
            time.sleep(et)
            et += et * 0.2
        
        dis_rdy = True
        ##global ex
        ##ex = True
#         print("launch file in DISABLE.py------------")
        # Takes 10s to exit after sys.exit called GPIOzero trying to close thread
        run(['python3', f'/home/pi/Desktop/Rover_Cam/modes/mode{m}.py'])


# press x many times within y seconds to diable, simple code for now
def enable():
    global bbp
    bbp += 1


led_dis = LED(26)

red_btn = Button(17, hold_time=2)
red_btn.when_held = shutdown
red_btn.when_released = reboot

# gray is to check mode, goto mode select, switch mode, and goto new mode
gray_btn = Button(27, hold_time=2)
gray_btn.when_held = goto_mode_select
# gray_btn.when_released = check_mode     #  Took out check_mode is susposed to also indicate that a mode is running

#if bb_used == True:
# blue is to turn off mode, or select, and later turn on start-up, make progamable code
blue_btn = Button(22)
#blue_btn.when_held =
blue_btn.when_released = enable


# For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
path_usb = path_usb.decode("utf-8").splitlines()[0]
path_usb = "/media/pi" + "/" + path_usb
# This should create a path to any removable storage ----------------------------------

pr = open(path_usb + "/RC_config.txt", "r")
prog = pr.read().splitlines()   # gets ride of the \n at end of each element
pr.close()

for i in prog:
    
    if i != "" and i[0:6] == "mode =":
        mode = int(i[6:])
    elif i != "" and i[0:24] == "disable_button_presses =":
        print(i[0:22])
        bb_presses = float(i[24:])
    elif i != "" and i[0:27] == "disable_button_time_frame =":
        print(i[0:27])
        bb_time_frame = float(i[27:])
    elif i != "" and i[0:19] == "lock_disable_time =":
        if "inf" in i[19:]:
            lock_disable_time = np.inf
        else:
            lock_disable_time = float(i[19:])

while True:
    time.sleep(0.1)
    
    if ex == True:
        exi()
    
    if bbp > 0:
        if bbp == 1 and des == 0:
#             print("in bbp == 1")
            bb_time = time.time() + bb_time_frame
            des = 1

        if time.time() > bb_time:
            des = 0
            if bbp == float(bb_presses):
#                 print("ex = true from ENABLE   SYS EXIT INSTEAD")
                
                dt = Thread(target=to_selected_mode)
                dt.daemon = True
                dt.start()
#                 to_selected_mode()
                while True:
                    time.sleep(0.1)
                    if dis_rdy == True:
                        time.sleep(0.5)
                        #ex = True

                        sys.exit()
        #                 break

            else:
#                 print("bb fail, in disable.py")
                time.sleep(lock_disable_time)
                bbp = 0











