
# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.
# Please see the LICENSE file that should have been included as part of this package.


import time
time.sleep(1)

import cv2
import numpy as np
import random
import sys
import os
from subprocess import run
from threading import Thread
from gpiozero import LED, Button
import RPi.GPIO as GPIO

was_held = False

mode = 3
ex = False
stop_check_mode = False
stop_reboot = False
play = False
bbp = 0
des = 0
bb_time = 0
fa_num = 0

bb_used = False
bb_pass = True

is_playing = False


# Subtract len of file name and / to get containing directory, and -6 more for "/modes"
rc_dir = os.path.abspath(__file__)
rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 7]

# # For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
# path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
# path_usb = path_usb.decode("utf-8").splitlines()[0]
# path_usb = "/media/pi" + "/" + path_usb
# # This should create a path to any removable storage ----------------------------------

pr = open(rc_dir + "/support/RC_config.txt", "r")
prog = pr.read().splitlines()   # gets ride of the \n at end of each element
pr.close()

a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
a7 = []
a8 = []

#a1 = np.where(prog[0] == "a")
for i in prog:
    if i != "" and i[0:2] == "a1":
        a1.append(i)
    elif i != "" and i[0:2] == "a2":
        a2.append(i)  
    elif i != "" and i[0:2] == "a3":
        a3.append(i)
    elif i != "" and i[0:2] == "a4":
        a4.append(i)
    elif i != "" and i[0:2] == "a5":
        a5.append(i)
    elif i != "" and i[0:2] == "a6":
        a6.append(i)
    elif i != "" and i[0:2] == "a7":
        a7.append(i)
    elif i != "" and i[0:2] == "a8":
        a8.append(i)  
    elif i != "" and i[0:10] == "set_time =":
        st = i[10:].split()
        yr = int(st[0])  # retrieved
        mo = int(st[1])
        da = int(st[2])
        hr = int(st[3])
        mi = int(st[4])
        se = int(st[5])
#         print(yr, mo, da, hr, mi, se)
         
    elif i != "" and i[0:12] == "play_audio =":
        if "y" in i[10:].lower():
            play = True
            audio = run(['ls', rc_dir + '/audio'], capture_output=True).stdout
            audio = audio.decode("utf-8").splitlines()
        else:
            audio = []
    elif i != "" and i[0:13] == "delay_audio =":
        delay_audio = float(i[13:])
    elif i != "" and i[0:20] == "use_disable_button =" and "y" in i[20:].lower():
        bb_used = True
    elif i != "" and i[0:24] == "disable_button_presses =":
        bb_presses = float(i[24:])
    elif i != "" and i[0:27] == "disable_button_time_frame =":
        bb_time_frame = float(i[27:])
    elif i != "" and i[0:13] == "start_delay =":
        start_delay = float(i[13:])
    elif i != "" and i[0:14] == "camera_index =":
        camera_index = int(i[14:])  
    elif i != "" and i[0:11] == "clip_time =":
        clip_time = float(i[11:])   
    elif i != "" and i[0:15] == "use_pi_camera =":
        if "y" in i[15:].lower():
            use_pi_camera = True
        else:
            use_pi_camera = False   
    elif i != "" and i[0:5] == "fps =":
        fps = float(i[5:])         
    elif i != "" and i[0:13] == "motion_area =":
        motion_area = float(i[13:])
    elif i != "" and i[0:13] == "motion_sens =":
        motion_sens = float(i[13:])
    elif i != "" and i[0:19] == "lock_disable_time =":
        if "inf" in i[19:]:
            lock_disable_time = np.inf
        else:
            lock_disable_time = float(i[19:])

if len(audio) == 0:
    play = False

a1h = []                    # list of a1 HIGH's
a1o = []                      # list of a1 LOW's
for i in a1:
    if "on" in i.lower():
        a1h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a1o.append(float(i.split()[-1]))

a1h.append(0)
a1o.append(0)

# Action 2
a2h = []                    # list of a1 HIGH's
a2o = []
for i in a2:
    if "on" in i.lower():
        a2h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a2o.append(float(i.split()[-1]))

a2h.append(0)
a2o.append(0)

# Action 3
a3h = []                    # list of a1 HIGH's
a3o = []
for i in a3:
    if "on" in i.lower():
        a3h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a3o.append(float(i.split()[-1]))

a3h.append(0)
a3o.append(0)

# Action 4
a4h = []                    # list of a1 HIGH's
a4o = []
for i in a4:
    if "on" in i.lower():
        a4h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a4o.append(float(i.split()[-1]))

a4h.append(0)
a4o.append(0)

# Action 5
a5h = []                    # list of a1 HIGH's
a5o = []
for i in a5:
    if "on" in i.lower():
        a5h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a5o.append(float(i.split()[-1]))

a5h.append(0)
a5o.append(0)

# Action 6
a6h = []                    # list of a1 HIGH's
a6o = []
for i in a6:
    if "on" in i.lower():
        a6h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a6o.append(float(i.split()[-1]))

a6h.append(0)
a6o.append(0)

# Action 7
a7h = []                    # list of a1 HIGH's
a7o = []
for i in a7:
    if "on" in i.lower():
        a7h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a7o.append(float(i.split()[-1]))

a7h.append(0)
a7o.append(0)

# Action 8
a8h = []                    # list of a1 HIGH's
a8o = []
for i in a8:
    if "on" in i.lower():
        a8h.append(float(i.split()[-1]))
    elif "off" in i.lower():
        a8o.append(float(i.split()[-1]))

a8h.append(0)
a8o.append(0)


# Load aoi pts list if any -----------------------------
p = open(rc_dir + "/support/aoi_pts.txt", "r")
p.readline()
pts = p.read().split()
p.close()

aoi_used = False
p_list = []

if len(pts) != 0:

    pts = list(map(int, pts))
    
    for idx, i in enumerate(pts):
        if idx % 4 == 0:
            p_list.append([pts[idx], pts[idx + 1], pts[idx + 2], pts[idx + 3]])
    compiled_overlay = np.zeros(shape=(480, 640, 1))  # gray img
    compiled_overlay = compiled_overlay + 255
    compiled_overlay = np.uint8(compiled_overlay)
    for i in p_list:
        compiled_overlay[i[0]:i[1], i[2]:i[3]] = 0

    aoi_used = True


# Action 1 pin is 12, act 2 is 16
# def runProg_a1(a1h, a1o):
def runAction(on_list, off_list, pin):      # now working  and does not effect vid   if stop file when HIGH will stay HIGH
#     print("Prog 1 run")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
#         GPIO.setup(act2, GPIO.OUT)
    time.sleep(0.01)
    ##GPIO.output(gled, GPIO.LOW)   # set default state, ..or not stopped file when on

    on_list_idx = 0
    off_list_idx = 0
    for i in max(on_list, off_list):        # max to iter based on longest list

        GPIO.output(pin, GPIO.LOW)

        time.sleep(off_list[off_list_idx])

        GPIO.output(pin, GPIO.HIGH)
        
        time.sleep(on_list[on_list_idx])   # a zero is appends to on on off lists

        if on_list_idx < len(on_list) - 1:
            on_list_idx += 1

        if off_list_idx < len(off_list) - 1:
            off_list_idx += 1
    GPIO.output(pin, GPIO.LOW)


def play_audio(aud, delay_aud):    # try with mp3 files
#     global audio
#     global delay_aud

    global is_playing
    is_playing = True

    time.sleep(delay_aud)
    for i in aud:      # plays one after other, all .wav and .py files in folder in alphabetical order
        if ".wav" in i:  # mp3, flac did not play well, only use .wav
#             run(['omxplayer', f'{rc_dir}/audio/{i}'])
            run(['aplay', f'{rc_dir}/audio/{i}'])
#    no work        run(['sudo', '-u', '"#1000"', 'XDG_RUNTIME_DIR=/run/user/1000', 'aplay', f'/home/pi/Desktop/Rover_Cam/audio/{i}'])
        if ".py" in i:
            run(['python3', f'{rc_dir}/audio/{i}'])
            
    is_playing = False



def exi():
    import sys
    GPIO.cleanup() # causes lot's faults on exit, at least when GPIO is not used, faults are ok.. here..
    # this file mode2 closes fast, maybe bc of this fault
    ca.release()
    time.sleep(0.5)
    # Takes 10s to exit after sys.exit called GPIOzero trying to close thread
    sys.exit()


def shutdown():           # has zombie thread issue
    global stop_reboot
    stop_reboot = True

    global ex
    ex = True

    run(['python3', rc_dir + '/support/shutdown.py'])
#         check_call(['sudo', 'poweroff'])  # old way


def reboot():
    global stop_reboot    # does not have zombie thread issue
    if stop_reboot == False:

        global ex
        ex = True

        run(['python3', rc_dir + '/support/reboot.py'])
#         check_call(['sudo', 'reboot'])  #old way


def goto_mode_select():          # has zombie thread issue
    global stop_check_mode
    stop_check_mode = True

    global ex
    ex = True

    run(['python3', rc_dir + '/support/mode-select.py'])
    # sys exit here closes only this thread, see os._exit() but have know how to use


def check_mode():   # zombie thread issue, also when in here blocks other btn presses
    global mode
    
    if stop_check_mode == False:
#             sys.exit()       # stops thread but may interfere with GPIOzero stop thead
        # blink led number of times equal to mode number
        for i in range(mode):
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
            
        clip_ind = run(["ls", sdate], capture_output=True).stdout
        clip_ind = clip_ind.decode("utf-8").splitlines()
        clip_ind = len(clip_ind)
        
        time.sleep(1)
        
        if clip_ind > 30:
            clip_ind = 30
        for i in range(clip_ind):
            led.on()
            time.sleep(0.26)
            led.off()
            time.sleep(0.26)


# press x many times within y seconds to disable, simple code for now
def disable():
    global bbp
    bbp += 1


def disable_inloop():
    
    # globals that arn't update can go here
    while True:
        time.sleep(0.1)
        global bbp
        global bb_presses
        global bb_time_frame
        global bb_time
        global fa_num
        global des
        global ex
        global lock_disable_time

        # ..is now working
        
        if bbp > 0:
            if bbp == 1 and des == 0:
                bb_time = time.time() + bb_time_frame
                des = 1

            if time.time() > bb_time:
                des = 0
                if bbp == float(bb_presses):
                    ex = True

                # ---- run await renable py file here -----
                    run(['python3', rc_dir + '/support/disable.py'])

                else:
                    # Log in the clips folder a txt file when a disable attempt fails
                    fa_num += 1
                    fa = open(rc_dir + f"/Clips/failed-btn-code-attempt-m3-{fa_num}.txt", "a")
                    fa.write("This file was created to inform you that the disable button was pressed at least once,")
                    fa.write("\n")
                    fa.write("and not the amount of times specified in the settings file, within the time frame.")
                    fa.write("\n")
                    fa.write(f"This has occured {fa_num} times.")
                    fa.write("\n")
                    fa.write(f"In mode 3, on run: {sdate}")
                    fa.close()
                    
                    time.sleep(lock_disable_time)                    
                    bbp = 0

led = LED(26)

# led.close()
# led.start()
# led = LED(26)

red_btn = Button(17, hold_time=2)
red_btn.when_held = shutdown
red_btn.when_released = reboot

# gray is to check mode, goto mode select, switch mode, and goto new mode
gray_btn = Button(27, hold_time=2)
gray_btn.when_held = goto_mode_select
gray_btn.when_released = check_mode

if bb_used == True:
    # blue is to turn off mode, or select, and later turn on start-up, make progamable code
    blue_btn = Button(22)
    #blue_btn.when_held =
    blue_btn.when_released = disable


# keep even in mode3 for use in disable_in_loop()
start = time.time() - (mi * 60) - se   # moved this to start-up.py
s = open(rc_dir + "/support/comm.txt", "r")
start = float(s.readline())
s.close()
m = 60

ran = random.randint(10000, 99000)

sdate = f"{yr}-{mo}-{da}-{hr}-{mi}-{se}"
sdate = sdate + "_" + str(ran)      # changed for mode 3
# run(['mkdir', sdate])              # commented out for mode 3

print(f'sdate : {sdate}')  


# Action 1 pin is 12, Action 2 is 16, etc
action1 = Thread(target=runAction, args=(a1h, a1o, 12))
action2 = Thread(target=runAction, args=(a2h, a2o, 16))
action3 = Thread(target=runAction, args=(a3h, a3o, 20))
action4 = Thread(target=runAction, args=(a4h, a4o, 21))
action5 = Thread(target=runAction, args=(a5h, a5o, 23))   # pins 0-8 are HIGH by defualt
action6 = Thread(target=runAction, args=(a6h, a6o, 24))
action7 = Thread(target=runAction, args=(a7h, a7o, 13))
action8 = Thread(target=runAction, args=(a8h, a8o, 19))

if play == True:
    t_audio = Thread(target=play_audio, args=(audio, delay_audio))

dt = Thread(target=disable_inloop)
dt.daemon = True
dt.start()

out_num = 0

# fourcc = cv2.VideoWriter_fourcc(* "XVID")


if use_pi_camera == False:
    # ca = cv2.VideoCapture("C:/Users/murph/Desktop/Graphic, Video, Blender/Blender Outputs/Cloth Ball3b9/Evvee Lossless 64 1-300 test.mp4")     # Load from any video file, change slashes
    ca = cv2.VideoCapture(camera_index)
    
    # Capping fps might be good for limiting fps, but causes actual clip time to be 1s less then set clip time
#     ca.set(cv2.CAP_PROP_FPS, fps)

    # fourcc code is the output video codec see https://www.fourcc.org/codecs.php   XVID = MPEG-4
    # uncomment to only cap motion in one file
    # out = cv2.VideoWriter('CamF-only-motion.avi', fourcc, 20.0, (640, 480))

    time.sleep(2)   # Camera sensor warm up
    time.sleep(start_delay)

    while ca.isOpened():

        ret, frame1 = ca.read()          # ret is retrieve is a variable for to bool that .read() returns

        # if cv2.waitKey(1000) == ord('1'):         # This seems to put a gap between the frames read
        #     break
        # ret, frame11 = ca.read()         #   added            # Adding more frames to read makes it notice very slow movement, while making it slower to react
        time.sleep(0.01)  #@ No need for all the copies using sleep has same effect
        ret, frame2 = ca.read()

        det = 0

        if ex == True:
            exi()

        # xx This is night vision helps detect in low light, though kinda detects too much where there's big light diff
        # xx only helps a bit in the dark, no longer seems to cause false detects in high light diff
        # frame1[:, :, 1] = np.where(frame1[:, :, 1] < 20, cv2.multiply(frame1[:, :, 1], 2), frame1[:, :, 1])
        # frame2[:, :, 1] = np.where(frame2[:, :, 1] < 20, cv2.multiply(frame2[:, :, 1], 2), frame1[:, :, 1])
        
        # Make thres adjust to highest light pixel, stops false dets in hight light areas,
        # and enables better motion det at lower light.
        npmax = np.max(frame1)
        npmax = npmax / 255
        th = 22 * npmax + motion_sens   # or up to 4   # good
        # th = 12 * npmax + 1  # or up to 4
        th = round(th, 0)

        if ret == True:                 # This makes sure there is a frame being read before a video gets written
            # print (ca.get(3))           # this gets the frame width 3 = cv2.CAP_PROP_FRAME_WIDTH
            # print (ca.get(4))           # this get the frame height 4 = cv2.CAP_PROP_FRAME_HEIGHT       list of all the Enumerators    https://docs.opencv.org/4.0.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
            # out.write(frame1)

            # frame1[:, :, :] = np.divide(frame1[:, :, :], 255)
            # frame2[:, :, :] = np.divide(frame2[:, :, :], 255)

            # Only really need absdiff for motion det, sum it and if > ...  No doesn't work a good
            #  because if there's much diff in one small area, then theres a contour, but sum diffs no changed
            diff = cv2.absdiff(frame1, frame2)      # imp could make this adjust to different light levels

            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            
    #         cv2.imshow("old gray", gray)
            if aoi_used == True:
                gray = cv2.subtract(gray, compiled_overlay)
    #             cv2.imshow("new gray", gray)
    #         cv2.waitKey(0)
            
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)

            # # --- Uncomment for Contours ----
            erode = cv2.erode(thresh, None, iterations=2)
            dilated = cv2.dilate(erode, None, iterations=2)  # imp threshold chooses what color value range to include
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #             cv2.drawContours(frame1, contours, -1, (0, 25, 255), 2)
            for c in contours:
                if cv2.contourArea(c) < motion_area:  # imp A smaller number here detects smaller objects moving, was orginally set at 5000, does it take moe processor power?
                    continue
    #                 x, y, w, h = cv2.boundingRect(c)
    #                 cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)
                det = 1

            if det == 1:

                # Action 1 pin is 16, act 2 is 12
                if not action1.is_alive() and not action2.is_alive() and not action3.is_alive() and not action4.is_alive() and not action5.is_alive() and not action6.is_alive() and not action7.is_alive() and not action8.is_alive():
                    action1 = Thread(target=runAction, args=(a1h, a1o, 12))    # works
                    action1.daemon = True  # TRY THIS  These thread prob stop when the prog ends
                        # don't see any extra in htop, and GPIOzero seems to be daemon default
                    action1.start()
                    action2 = Thread(target=runAction, args=(a2h, a2o, 16))   
                    action2.daemon = True
                    action2.start()
                    action3 = Thread(target=runAction, args=(a3h, a3o, 20))    
                    action3.daemon = True
                    action3.start()
                    action4 = Thread(target=runAction, args=(a4h, a4o, 21))    
                    action4.daemon = True
                    action4.start()
                    action5 = Thread(target=runAction, args=(a5h, a5o, 23))    
                    action5.daemon = True
                    action5.start()
                    action6 = Thread(target=runAction, args=(a6h, a6o, 24))   
                    action6.daemon = True
                    action6.start()
                    action7 = Thread(target=runAction, args=(a7h, a7o, 13))   
                    action7.daemon = True
                    action7.start()
                    action8 = Thread(target=runAction, args=(a8h, a8o, 19))    
                    action8.daemon = True
                    action8.start()

                    if play == True and is_playing == False:
                        t_audio = Thread(target=play_audio, args=(audio, delay_audio))
                        t_audio.daemon = True
                        t_audio.start()

        else:
            break


    ca.release()               # Stops the capture, don't see a difference
    # cv2.destroyAllWindows()         # destroys window, window stops without this, don't see a difference


else:
    # -- Pi Cam Start ---
    
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    
    # Working rec 6s clips when clip time set to 5s
    # Seems like still got same fram rate/ clip time issuse
    
    # Higher fps makes clip shorter
    # is close to various clip times if fps is low (10), maybe 1s shorter
    # even at 24 fps, but 45 fps messes up, try on zero with low fps
    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = fps
    rawCapture = PiRGBArray(camera, size=(640, 480))

    time.sleep(2)   # Camera sensor warm up
    time.sleep(start_delay)
    
    cnt = 0
    
    pi_cap = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
            
#     time_e = time.time()
#     time_p = 0
    
#     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    for frame in pi_cap:

        frame1 = frame.array

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
         
#         if time_e > 1./fps:         # doesn't seem to help
#             time_p = time.time()
        
        det = 0

        if ex == True:
            exi()

        # xx This is night vision helps detect in low light, though kinda detects too much where there's big light diff
        # xx only helps a bit in the dark, no longer seems to cause false detects in high light diff
        # frame1[:, :, 1] = np.where(frame1[:, :, 1] < 20, cv2.multiply(frame1[:, :, 1], 2), frame1[:, :, 1])
        # frame2[:, :, 1] = np.where(frame2[:, :, 1] < 20, cv2.multiply(frame2[:, :, 1], 2), frame1[:, :, 1])

        npmax = np.max(frame1)
        npmax = npmax / 255
        th = 22 * npmax + motion_sens   # or up to 4   # good
        # th = 12 * npmax + 1  # or up to 4
        th = round(th, 0)

        if cnt == 0:
            cnt = 1
            frame2 = frame1

        if cnt == 1:

            # print (ca.get(3))           # this gets the frame width 3 = cv2.CAP_PROP_FRAME_WIDTH
            # print (ca.get(4))           # this get the frame height 4 = cv2.CAP_PROP_FRAME_HEIGHT       list of all the Enumerators    https://docs.opencv.org/4.0.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
            # out.write(frame1)

            # frame1[:, :, :] = np.divide(frame1[:, :, :], 255)
            # frame2[:, :, :] = np.divide(frame2[:, :, :], 255)

            # Only really need absdiff for motion det, sum it and if > ...  No doesn't work a good
            #  because if there's much diff in one small area, then theres a contour, but sum diffs no changed
            diff = cv2.absdiff(frame1, frame2)      # imp could make this adjust to different light levels

            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            
            if aoi_used == True:
                gray = cv2.subtract(gray, compiled_overlay)
            
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)

            # # --- Uncomment for Contours ----
            erode = cv2.erode(thresh, None, iterations=2)
            dilated = cv2.dilate(erode, None, iterations=2)  # imp threshold chooses what color value range to include
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #             cv2.drawContours(frame1, contours, -1, (0, 25, 255), 2)
            for c in contours:
                if cv2.contourArea(c) < motion_area:  # imp A smaller number here detects smaller objects moving, was orginally set at 5000, does it take moe processor power?
                    continue
    #                 x, y, w, h = cv2.boundingRect(c)
    #                 cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)
                det = 1
                
            frame2 = frame1                 # this can work should do not in while loop
    #         cv2.imshow("Frame2", frame2)

            if det == 1:

                # Action 1 pin is 16, act 2 is 12
                if not action1.is_alive() and not action2.is_alive() and not action3.is_alive() and not action4.is_alive() and not action5.is_alive() and not action6.is_alive() and not action7.is_alive() and not action8.is_alive():
                    action1 = Thread(target=runAction, args=(a1h, a1o, 12))    # works
                    action1.daemon = True  # TRY THIS  These thread prob stop when the prog ends
                        # don't see any extra in htop, and GPIOzero seems to be daemon default
                    action1.start()
                    action2 = Thread(target=runAction, args=(a2h, a2o, 16))   
                    action2.daemon = True
                    action2.start()
                    action3 = Thread(target=runAction, args=(a3h, a3o, 20))    
                    action3.daemon = True
                    action3.start()
                    action4 = Thread(target=runAction, args=(a4h, a4o, 21))    
                    action4.daemon = True
                    action4.start()
                    action5 = Thread(target=runAction, args=(a5h, a5o, 23))    
                    action5.daemon = True
                    action5.start()
                    action6 = Thread(target=runAction, args=(a6h, a6o, 24))   
                    action6.daemon = True
                    action6.start()
                    action7 = Thread(target=runAction, args=(a7h, a7o, 13))   
                    action7.daemon = True
                    action7.start()
                    action8 = Thread(target=runAction, args=(a8h, a8o, 19))    
                    action8.daemon = True
                    action8.start()

                    if play == True and is_playing == False:
                        t_audio = Thread(target=play_audio, args=(audio, delay_audio))
                        t_audio.daemon = True
                        t_audio.start()




    
    
    
