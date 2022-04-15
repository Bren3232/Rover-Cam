#!/usr/bin/env python3


# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.


try:
    import time
    time.sleep(40)    # set to about 40s *****

    import sys
    from subprocess import check_call, call, run
#     import os
    from threading import Thread
    
    starr = time.time()   # Clock in mode files is based on this
    
#     os.setuid(1000)
#     os.setgid(1000)

    # For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
    path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
    path_usb = path_usb.decode("utf-8").splitlines()[0]
    path_usb = "/media/pi" + "/" + path_usb
    # This should create a path to any removable storage ----------------------------------

    f = open(path_usb + "/RC_config.txt", "r")
    prog = f.read().splitlines()   # gets ride of the \n at end of each element
#     print(prog)
    for i in prog:
        if "mode =" in i:
            m = i.split()
            m = int(m[-1])
            
        elif i != "" and i[0:10] == "set_time =":
            st = i[10:].split()
#             print("st is: ", st)
            yr = int(st[0])  # retrieved
            mo = int(st[1])
            da = int(st[2])
            hr = int(st[3])
            mi = int(st[4])
            se = int(st[5])
            print(mi, se)     

    f.close()
    
    
    start = starr - (mi * 60) - se   # moving this to start-up.py from mode
    s = open("/home/pi/Desktop/Rover_Cam/comm.txt", "a")
    s.truncate(0)
    s.write(str(start))
    s.close()
    

    def launch_file():     # works here and closes threads fast with gray btn, but except triggers
    #         GPIO.cleanup()
#         print("launch file in start-up.py------------")
        global m
#         time.sleep(3)
        # Takes 10s to exit after sys.exit called GPIOzero trying to close thread
#         sys.exit()
        
#         run(["exit"], shell=True)
        run(['python3', f'/home/pi/Desktop/Rover_Cam/modes/mode{m}.py'])
#         time.sleep(3)
#         sys.exit()


#     print('HERE BEFORE Call')
    t = Thread(target=launch_file)
    t.daemon = True
    t.start()
#     run(['python3', f'/home/pi/Desktop/Rover_Cam/mode{m}.py'])
#     print('HERE AFTER Call')
    time.sleep(5)  # make sure launch_file() finnishs first
#     sys.exit()


except:
#     import sys
#     from subprocess import check_call
#     failed = "/home/pi/Desktop/FAILED-SecCamf-Rover_Cam"
#     check_call(['mkdir', failed])
#     failed = "/home/pi/Desktop/FAILED-start-up.txt"
#     check_call(['touch', failed])
    fa =  open("/home/pi/Desktop/FAILED-start-up.txt", "a")
    fa.write("This file was created to inform you that" +
    " /home/pi/Desktop/Rover_Cam/Run-at-startup/start-up.py has failed to run.\n" +
    "Delete this file and try again. If the problem presists, try increasing the\n" +
    "the number passed into the first occurence of 'time.sleep()'\n" +
    "in the file mentioned.******&&&&&&&&&")
    fa.close()
#     sys.exit()



