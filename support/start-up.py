
# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.
# Please see the LICENSE file that should have been included as part of this package.

# If running this file for testing run from inside "/Run-at-startup".

try:
    import time
    time.sleep(2)    # sleep for 40s in crontab

    import sys
    import os
    from subprocess import run, call
#     import os
    from threading import Thread
    
    starr = time.time()   # Clock in mode files is based on this
    
#     os.setuid(1000)
#     os.setgid(1000)

    # Subtract len of file name and / to get containing directory, and -15 more for "/Run-at-startup"
    rc_dir = os.path.abspath(__file__)
    if "Run-at-start" in rc_dir:
        rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 16]
    else:
        rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 9]

#     # For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
#     path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
#     path_usb = path_usb.decode("utf-8").splitlines()[0]
#     path_usb = "/media/pi" + "/" + path_usb
#     # This should create a path to any removable storage ----------------------------------

    f = open(rc_dir + "/support/RC_config.txt", "r")
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

    f.close()
    
    
    start = starr - (mi * 60) - se   # For Clock

    s = open(rc_dir + "/support/comm.txt", "a")
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
        run(['python3', f'{rc_dir}/modes/mode{m}.py'])
#         time.sleep(3)
#         sys.exit()


#     print('HERE BEFORE Call')
    t = Thread(target=launch_file)
    t.daemon = True
    t.start()
    time.sleep(5)  # make sure launch_file() finnishs first


except:
#     import sys
#     from subprocess import check_call
#     failed = "/home/pi/Desktop/FAILED-SecCamf-Rover_Cam"
#     check_call(['mkdir', failed])
#     failed = "/home/pi/Desktop/FAILED-start-up.txt"
#     check_call(['touch', failed])
    fa =  open(rc_dir + "/FAILED-start-up.txt", "a")
    fa.write("This file was created to inform you that" +
    " in Rover Cam directory /Run-at-startup/start-up.py has failed to run.\n" +
    "Delete this file and try again. If the problem presists, try increasing the\n" +
    "the number passed into the first occurence of 'time.sleep()'\n" +
    "in the file mentioned.")
    fa.close()
#     sys.exit()



