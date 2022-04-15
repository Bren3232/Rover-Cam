#!/usr/bin/env python3


# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.


from tkinter import *
from tkinter import ttk
# from tkinter import font
import tkinter.font as tkFont
# from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno
from subprocess import run
from threading import Thread
import time
import sys

import cv2
import im_resize as imr
import numpy as np
from PIL import ImageTk, Image
import PIL


root = Tk()

root.geometry("880x850")
root.title(" tk-sett ")
# ff = font.families()       # gets all available fonts
# print(ff)
# root.iconbitmap('test-icon.ico')     # adding icon is fucking up scroll
# root.iconphoto(False, PhotoImage(file='test-icon.png'))
# root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='/path/to/ico/icon.png')

loaded = False

# if loaded == True:
sett = {}
a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
a7 = []
a8 = []
save_it = False
scr2_entered = False
scr3_entered = False

def popup_alert_usb():
    showinfo("Error", '''Could not find a USB storage device in "/media/pi/". Make sure a USB
                is plugged in.''')
    sys.exit()
    
def popup_alert_usb_files():
    ask = askyesno("Error", '''Could not load the nessesary files, RC_config.txt, and aoi_pts.txt on storage
device. Would you like to copy these files to the USB device? Program will need to be restarted.''')
    if ask == True:
        run(["cp", "/home/pi/Desktop/Rover_Cam/RC_config.txt", path_usb])
        run(["cp", "/home/pi/Desktop/Rover_Cam/aoi_pts.txt", path_usb])
    root.destroy()   # restart instead of reload, because aoi img not packed, will shorten scroll down
#         load_all()

def popup_alert_usb_save():
    showinfo("Error", "Could not find/save to files on storage device. Make sure a usb is plugged in and contains the RC_config.txt file.")

def popup_alert_vid():
    showinfo("Error", "Video Stream failed, try another camera index")   # makes an alert "ding" noise, in windows at least

try:
    # For finding the path to usb storage by looking in /media/pi, where is standard place where removable drives mount.
    path_usb = run(["ls", "/media/pi"], capture_output=True).stdout
    path_usb = path_usb.decode("utf-8").splitlines()[0]
    path_usb = "/media/pi" + "/" + path_usb
except:
    popup_alert_usb()
#     print('path_usb = path_usb.decode  utf-8 .splitlines[0] IndexError: list index out of range')


def load_all():
    global sett
    global a1
    global a2
    global a3
    global a4
    global a5
    global a6
    global a7
    global a8
    global aoi_img
    global compiled_overlay
    global plimg_h
    global p_list_save
    global p_list
    global ao_im
    global boot_on
    global play_audio
    global use_disable
#     print("in load_all")

    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []

    try:
        pr = open(path_usb + "/RC_config.txt", "r")
        prog = pr.read().splitlines()   # gets ride of the \n at end of each element
    #     prog = pr.read().decode("utf-8").splitlines()
    #     prog = prog.splitlines()
        pr.close()

        #a1 = np.where(prog[0] == "a")
        for i in prog:

            if i != "" and i[0:10] == "set_time =":
                st = i[10:].split()
    #             print("st is: ", st)
                sett["yr"] = st[0] # retrieved
                sett["mo"] = st[1]
                sett["da"] = st[2]
                sett["hr"] = st[3]
                sett["mi"] = st[4]
                sett["se"] = st[5]

            elif i != "" and i[0:20] == "run_at_system_boot =":
    #             print(i, "ooooooo")
                if "Y" in i[20:]:
                    sett["run_at_system_boot"] = "Y"
                    boot_on = False
                    boot_tog.config(image=tog_on)
                else:
                    sett["run_at_system_boot"] = "N"
                    boot_on = True
                    boot_tog.config(image=tog_off)

            elif i != "" and i[0:11] == "clip_time =":
                sett["clip_time"] = i[11:].strip()
                
            elif i != "" and i[0:15] == "use_pi_camera =":
                if "Y" in i[15:]:
                    sett["use_pi_camera"] = "Y"
                    picam_on = False
                    picam_tog.config(image=tog_on)
                else:
                    sett["use_pi_camera"] = "N"
                    picam_on = True
                    picam_tog.config(image=tog_off)
                    
            elif i != "" and i[0:5] == "fps =":
                sett["fps"] = i[5:].strip()
            
            elif i != "" and i[0:13] == "motion_area =":
                sett["motion_area"] = i[13:].strip()
            elif i != "" and i[0:13] == "motion_sens =":
                sett["motion_sens"] = i[13:].strip()
            elif i != "" and i[0:6] == "mode =":
                sett["mode"] = i[6:].strip()

            elif i != "" and i[0:12] == "play_audio =":
    #             print(i, "ooooooo")
                if "Y" in i[12:]:
                    sett["play_audio"] = "Y"
                    play_audio = False
                    audio_tog.config(image=tog_on)
                else:
                    sett["play_audio"] = "N"
                    play_audio = True
                    audio_tog.config(image=tog_off)

            elif i != "" and i[0:13] == "delay_audio =":
                sett["delay_audio"] = i[13:].strip()

    #         elif i != "" and i[0:20] == "use_disable_button =":
    #             if "Y" in i[20:]:
    #                 sett["use_disable_button"] = "Y"
    #             else:
    #                 sett["use_disable_button"] = "N"

            elif i != "" and i[0:20] == "use_disable_button =":
    #             print(i, "ooooooo")
                if "Y" in i[20:]:
                    sett["use_disable_button"] = "Y"
                    use_disable = False
                    disable_tog.config(image=tog_on)
                else:
                    sett["use_disable_button"] = "N"
                    use_disable = True
                    disable_tog.config(image=tog_off)

            elif i != "" and i[0:24] == "disable_button_presses =":
                sett["disable_button_presses"] = i[24:].strip()
            elif i != "" and i[0:27] == "disable_button_time_frame =":
                sett["disable_button_time_frame"] = i[27:].strip()
            elif i != "" and i[0:19] == "lock_disable_time =":
                sett["lock_disable_time"] = i[19:].strip()
            elif i != "" and i[0:13] == "start_delay =":
                sett["start_delay"] = i[13:].strip()
            elif i != "" and i[0:14] == "camera_index =":
                sett["camera_index"] = i[14:].strip()


            elif i != "" and i[0:2] == "a1":
        #     if "a1" in i.lower():
                a1.append(i[2:].strip())

            elif i != "" and i[0:2] == "a2":
        #     if "a1" in i.lower():
                a2.append(i[2:].strip())

            elif i != "" and i[0:2] == "a3":
        #     if "a1" in i.lower():
                a3.append(i[2:].strip())

            elif i != "" and i[0:2] == "a4":
        #     if "a1" in i.lower():
                a4.append(i[2:].strip())


            elif i != "" and i[0:2] == "a5":
        #     if "a1" in i.lower():
                a5.append(i[2:].strip())

            elif i != "" and i[0:2] == "a6":
        #     if "a1" in i.lower():
                a6.append(i[2:].strip())

            elif i != "" and i[0:2] == "a7":
        #     if "a1" in i.lower():
                a7.append(i[2:].strip())

            elif i != "" and i[0:2] == "a8":
        #     if "a1" in i.lower():
                a8.append(i[2:].strip())



        # load aoi
    #     ao_i = cv2.imread(path_usb + "/aoi.png")
    #
    #     # SHOULD SAVED AND LOAD THE p_list INSTEAD
    #     cond = (ao_i[:, :, 0] == 0) & (ao_i[:, :, 1] == 0) & (ao_i[:, :, 2] == 0)
    #
    #     ao_i[cond] = [1, 254, 1]
    #     ao_i[cond == False] = [0, 0, 0]

    #     try:
    #         p_list = p_list_save
    #     except:
    #         print("No  p_list_save")

        p = open(path_usb + "/aoi_pts.txt", "r")
        p.readline()
        pts = p.read().split()
        p.close()

        # ALL SEEMS WORKING MORE TESTING

        plimg_h = 240
        p_list = []

        if len(pts) != 0:

            pts = list(map(int, pts))
        #     print("p listy is  ", p_listy)
            for idx, i in enumerate(pts):
                if idx % 4 == 0:
                    p_list.append([pts[idx], pts[idx + 1], pts[idx + 2], pts[idx + 3]])

        #     pp = pts[0:4:3]

    #         ao_i = cv2.imread("/home/pi/Desktop/Rover_Cam/tk-stuff/aoi_sml.png")
            # --- p_list is made for 480x640 imgs ----

    #         compiled_overlay = np.zeros_like(ao_i)
            compiled_overlay = np.zeros(shape=(480, 640, 3))
            compiled_overlay = compiled_overlay + 20
            compiled_overlay = np.uint8(compiled_overlay)
            for i in p_list:
                compiled_overlay[i[0]:i[1], i[2]:i[3]] = [1, 170, 1]
    #             print('i ', i)
            #OR
    #         for idx, i in enumerate(p_list):
    #             cv2.rectangle(compiled_overlay, (p_list[:, idx], p_list[:, idx + 1]), (p_list[:, idx + 2], p_list[:, idx + 3]), (1, 254, 1), -1)

    #         cv2.imshow("compiled ", compiled_overlay)
    #         cv2.waitKey(0)

            compiled_overlay = imr.resize(compiled_overlay, height=plimg_h)

    #         ao_im = imr.resize(ao_i, height=plimg_h)
            ao_im = ImageTk.PhotoImage(Image.fromarray(compiled_overlay))
        else:
            ao_im = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Rover_Cam/aoi_sml.png"))

            compiled_overlay = np.zeros(shape=(480, 640, 3))
            compiled_overlay = np.uint8(compiled_overlay)

        aoi_img.config(image=ao_im)
        aoi_img.image = ao_im

    except:
        popup_alert_usb_files()
#         print('Couldnt find one or more files on the usb')


def load_btn():
    global sett
    global a1
    global a2
    global a3
    global a4
    global a5
    global a6
    global a7
    global a8


    load_all()                      # in case of save then load
    s1_txt.delete("1.0", END)
    fps_txt.delete("1.0", END)
    s2_txt.delete("1.0", END)
    s3_txt.delete("1.0", END)
    s4_txt.delete("1.0", END)
#     s5_txt.delete("1.0", END)
    s6_txt.delete("1.0", END)
#     s7_txt.delete("1.0", END)
    s8_txt.delete("1.0", END)
    s9_txt.delete("1.0", END)
    s10_txt.delete("1.0", END)
    s11_txt.delete("1.0", END)
    s12_txt.delete("1.0", END)

    st_txtyr.delete("1.0", END)
    st_txtmo.delete("1.0", END)
    st_txtda.delete("1.0", END)
    st_txthr.delete("1.0", END)
    st_txtmi.delete("1.0", END)
    st_txtse.delete("1.0", END)


    a_txt1.delete("1.0", END)
    a_txt2.delete("1.0", END)
    a_txt3.delete("1.0", END)
    a_txt4.delete("1.0", END)
    a_txt5.delete("1.0", END)
    a_txt6.delete("1.0", END)
    a_txt7.delete("1.0", END)
    a_txt8.delete("1.0", END)
    # clear(s3_txt)
    s1_txt.insert(END, sett["clip_time"])
    fps_txt.insert(END, sett["fps"])
    s2_txt.insert(END, sett["motion_area"])
    s3_txt.insert(END, sett["motion_sens"])
    s4_txt.insert(END, sett["mode"])
#     s5_txt.insert(END, sett["play_audio"])
    s6_txt.insert(END, sett["delay_audio"])
#     s7_txt.insert(END, sett["use_disable_button"])
    s8_txt.insert(END, sett["disable_button_presses"])
    s9_txt.insert(END, sett["disable_button_time_frame"])
    s10_txt.insert(END, sett["lock_disable_time"])
    s11_txt.insert(END, sett["start_delay"])
    s12_txt.insert(END, sett["camera_index"])

    st_txtyr.insert(END, sett["yr"])
    st_txtmo.insert(END, sett["mo"])
    st_txtda.insert(END, sett["da"])
    st_txthr.insert(END, sett["hr"])
    st_txtmi.insert(END, sett["mi"])
    st_txtse.insert(END, sett["se"])


#     print("a4  in load btn interting ", a4)
    for i in a1:
        a_txt1.insert(END, i  + "\n")
    for i in a2:
        a_txt2.insert(END, i  + "\n")
    for i in a3:
        a_txt3.insert(END, i  + "\n")
    for i in a4:
        a_txt4.insert(END, i  + "\n")
    for i in a5:
        a_txt5.insert(END, i  + "\n")
    for i in a6:
        a_txt6.insert(END, i  + "\n")
    for i in a7:
        a_txt7.insert(END, i  + "\n")
    for i in a8:
        a_txt8.insert(END, i  + "\n")



def save_btn():
    global p_list
    global sett

    sett["clip_time"] = s1_txt.get("1.0", "end-1c")
    sett["fps"] = fps_txt.get("1.0", "end-1c")
    sett["motion_area"] = s2_txt.get("1.0", "end-1c")
    sett["motion_sens"] = s3_txt.get("1.0", "end-1c")
    sett["mode"] = s4_txt.get("1.0", "end-1c")
#     sett["play_audio"] = s5_txt.get("1.0", "end-1c")
    sett["delay_audio"] = s6_txt.get("1.0", "end-1c")
#     sett["use_disable_button"] = s7_txt.get("1.0", "end-1c")
    sett["disable_button_presses"] = s8_txt.get("1.0", "end-1c")
    sett["disable_button_time_frame"] = s9_txt.get("1.0", "end-1c")
    sett["lock_disable_time"] = s10_txt.get("1.0", "end-1c")
    sett["start_delay"] = s11_txt.get("1.0", "end-1c")
    sett["camera_index"] = s12_txt.get("1.0", "end-1c")

    sett["yr"] = st_txtyr.get("1.0", "end-1c")
    sett["mo"] = st_txtmo.get("1.0", "end-1c")
    sett["da"] = st_txtda.get("1.0", "end-1c")
    sett["hr"] = st_txthr.get("1.0", "end-1c")
    sett["mi"] = st_txtmi.get("1.0", "end-1c")
    sett["se"] = st_txtse.get("1.0", "end-1c")


    a1_str = a_txt1.get("1.0", "end-1c")
    a1 = a1_str.splitlines()

    a2_str = a_txt2.get("1.0", "end-1c")
    a2 = a2_str.splitlines()

    a3_str = a_txt3.get("1.0", "end-1c")
    a3 = a3_str.splitlines()

    a4_str = a_txt4.get("1.0", "end-1c")
    a4 = a4_str.splitlines()

    a5_str = a_txt5.get("1.0", "end-1c")
    a5 = a5_str.splitlines()

    a6_str = a_txt6.get("1.0", "end-1c")
    a6 = a6_str.splitlines()

    a7_str = a_txt7.get("1.0", "end-1c")
    a7 = a7_str.splitlines()

    a8_str = a_txt8.get("1.0", "end-1c")
    a8 = a8_str.splitlines()

    try:
        f = open(path_usb + "/RC_config.txt", "r")
        fl = f.read().splitlines()
        f.close()

        a1_once = True

        for idx, i in enumerate(fl):
            # get 1st idx of fl that is "a1"
            if i[:8] == "Actions:" and a1_once == True:
                a1_fl_idx = idx
                a1_once = False

            if i != "" and i[0:10] == "set_time =":
    #             st = i[10:].split()
                fl[idx] = f'set_time = {sett["yr"]} {sett["mo"]} {sett["da"]} {sett["hr"]} {sett["mi"]} {sett["se"]}'

            elif i != "" and i[0:20] == "run_at_system_boot =":
                fl[idx] = "run_at_system_boot = " + sett["run_at_system_boot"].strip()
                f_check = run(["ls", "/home/pi/Desktop/Rover_Cam/Run-at-startup"], capture_output=True).stdout
                if sett["run_at_system_boot"] == "Y":
                    run(["cp", "/home/pi/Desktop/Rover_Cam/start-up.py",
                         "/home/pi/Desktop/Rover_Cam/Run-at-startup"])
                else:
                    if len(f_check) != 0:
                        run(["rm", "/home/pi/Desktop/Rover_Cam/Run-at-startup/start-up.py"])

            elif i != "" and i[0:11] == "clip_time =":
                fl[idx] = "clip_time = " + sett["clip_time"].strip()
                
            elif i != "" and i[0:15] == "use_pi_camera =":
                fl[idx] = "use_pi_camera = " + sett["use_pi_camera"].strip()               
            
            elif i != "" and i[0:5] == "fps =":
                fl[idx] = "fps = " + sett["fps"].strip()
            
            elif i != "" and i[0:13] == "motion_area =":
                fl[idx] = "motion_area = " + sett["motion_area"].strip()
            elif i != "" and i[0:13] == "motion_sens =":
                fl[idx] = "motion_sens = " + sett["motion_sens"].strip()
            elif i != "" and i[0:6] == "mode =":
                fl[idx] = "mode = " + sett["mode"].strip()

            elif i != "" and i[0:12] == "play_audio =":
                fl[idx] = "play_audio = " + sett["play_audio"].strip()

            elif i != "" and i[0:13] == "delay_audio =":
                fl[idx] = "delay_audio = " + sett["delay_audio"].strip()
            elif i != "" and i[0:20] == "use_disable_button =":
                fl[idx] = "use_disable_button = " + sett["use_disable_button"].strip()
            elif i != "" and i[0:24] == "disable_button_presses =":
                fl[idx] = "disable_button_presses = " + sett["disable_button_presses"].strip()
            elif i != "" and i[0:27] == "disable_button_time_frame =":
                fl[idx] = "disable_button_time_frame = " + sett["disable_button_time_frame"].strip()
            elif i != "" and i[0:19] == "lock_disable_time =":
                fl[idx] = "lock_disable_time = " + sett["lock_disable_time"].strip()
            elif i != "" and i[0:13] == "start_delay =":
                fl[idx] = "start_delay = " + sett["start_delay"].strip()
            elif i != "" and i[0:14] == "camera_index =":
                fl[idx] = "camera_index = " + sett["camera_index"].strip()

        fl = fl[:a1_fl_idx + 1]
        fl.append("")

    #     fl.append("- Actions: allways start in off state, 0's and decimals acceptable.")
        if len(a1) > 0:
            for i in a1:
                fl.append("a1 " + i)

        fl.append("")

        if len(a2) > 0:
            for i in a2:
                fl.append("a2 " + i)
        fl.append("")

        if len(a3) > 0:
            for i in a3:
                fl.append("a3 " + i)
        fl.append("")

        if len(a4) > 0:
            for i in a4:
                fl.append("a4 " + i)
        fl.append("")

        if len(a5) > 0:
            for i in a5:
                fl.append("a5 " + i)
        fl.append("")

        if len(a6) > 0:
            for i in a6:
                fl.append("a6 " + i)
        fl.append("")

        if len(a7) > 0:
            for i in a7:
                fl.append("a7 " + i)
        fl.append("")

        if len(a8) > 0:
            for i in a8:
                fl.append("a8 " + i)

        f2 = open(path_usb + "/RC_config.txt", "w")
        f2.truncate(0)
        for i in fl:           #xx   fl is a list
            f2.write(str(i) + "\n")  # working  now just to do the layout and vars
        f2.close()  # should ask to save settings on close if not saved?

        p = open(path_usb + "/aoi_pts.txt", "w")
    #     pts = p.read().split()
        p.write("This is place holder text")
        for i in p_list:
            for j in i:
                p.write(str(j) + " ")
        p.close()

    except:
        popup_alert_usb_save()
#         print('couldnt find or open files on usb to save')


# Start of my selectAOI, maybe add to cvtools     --------------------
p1x = 0
p1y = 0
p2x = 0
p2y = 0
p_list = []
down = False
start_aoi = False
end_aoi = False
brk_loop = False

# To always save an aoi.png, if this not changed then aoi is not used, sum would be 235008000.0
# ...can use sum an aoi'd img could only have slightest possibility of matching if cam img is taller
# final_aoi = np.ones((480, 640, 3), dtype=np.uint8) * 255
final_aoi = np.zeros((11, 2, 3), dtype=np.uint8)

def select_aoi():
    # import cv2
    global end_aoi
    global compiled_overlay
    global final_aoi
#     global aoi_img

    global img2
    global p_list
    global plimg_h

    global brk_loop

    cap = cv2.VideoCapture(int(sett["camera_index"]))

    if not cap.isOpened():  # works and pauses code until window is closed
        brk_loop = True
        popup_alert_vid()

    def click_event(event, x, y, flags, param):
        global p1x
        global p1y
        global p2x
        global p2y
        global p_list
        global down
        global start_aoi  # just for play
        global end_aoi
        global brk_loop


        if event == cv2.EVENT_RBUTTONDOWN:
            brk_loop = True

        if event == cv2.EVENT_LBUTTONDOWN:
            start_aoi = True
            down = True

            p1x = x
            p1y = y
            p2x = x
            p2y = y

        if event == cv2.EVENT_MOUSEMOVE and down == True:  # Is current mouse location

            if x < 0:  # Stop from going negative
                x = 0
            if y < 0:  # minus border / plus border - cv2.copyMakeBorder  not using
                y = 0

            if x > img.shape[1]:  # Stop from going over img size
                x = img.shape[1]
            if y > img.shape[0]:
                y = img.shape[0]
            p2x = x
            p2y = y

        if event == cv2.EVENT_LBUTTONUP:  # param prints None, flags 0
            down = False
            end_aoi = True

    alpha = 0.4
    try:
        compiled_overlay = imr.resize(compiled_overlay, height=480)
    except:
        pass
    # --------------------------------------------
    while cap.isOpened():
    # while True:
        time.sleep(0.02)
        ret, img = cap.read()

        # img = cv2.imread("aoi_sml2.png")
        # ret = True

        if ret == True:
        # My AOI   won't be able to use tk window  --------------------
            img = imr.resize(img, 640)     # will have to save this or do calculations if having different res options
                                                # would resize the mask to frame size, easiest way
            overlay = img.copy()
            try:
                overlay = cv2.addWeighted(overlay, alpha, compiled_overlay, 1 - alpha, 0)
            except:
                pass

            if down == True or end_aoi == True:
                # cv2.rectangle(img, (p1x, p1y), (p2x, p2y), (0, 255, 0), 2)
                cv2.rectangle(overlay, (p1x, p1y), (p2x, p2y), (0, 255, 0), -1)  # save overlay to add to final, or use cords
                img2 = img.copy()
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            else:
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

#             img4 = cv2.copyMakeBorder(img, 40, 40, 40, 40, borderType=cv2.BORDER_CONSTANT, value=0)

            cv2.imshow('Select AOI - Right Click To Cancel', img)
            cv2.setMouseCallback('Select AOI - Right Click To Cancel', click_event)  # does not stop code, has to be after imshow

            if end_aoi == True:
                end_aoi = False
                break

            if brk_loop == True:
                break

            cv2.waitKey(1)

#             if cv2.waitKey(1) & 0xFF == ord('q'):    # take out
#                 break
        else:
            break

    if brk_loop == False:

        # My AOI    --------------------------
        pminy = min(p1y, p2y)
        pmaxy = max(p1y, p2y)
        pminx = min(p1x, p2x)
        pmaxx = max(p1x, p2x)

        p_list.append([pminy, pmaxy, pminx, pmaxx])
#         print(p_list)

        # img2 = img[pminy:pmaxy, pminx:pmaxx]
        # cv2.imshow("img2", img2)

        compiled_overlay = np.zeros_like(img)
        for i in p_list:
            compiled_overlay[i[0]:i[1], i[2]:i[3]] = [1, 254, 1]
        #OR
    #     for idx, i in enumerate(p_list):
    #         cv2.rectangle(compiled_overlay, (p_list[idx], p_list[idx + 1]), (p_list[idx + 2], p_list[idx + 3]), (1, 254, 1), -1)

        final_aoi = compiled_overlay.copy()
        final_aoi[final_aoi == 0] = 255
        final_aoi[final_aoi != 255] = 0    # cv2.sub from diff
        # final_aoi = cv2.subtract(img, final_aoi)   # test
        # cv2.imshow("aoi", final_aoi)
        img2 = cv2.addWeighted(compiled_overlay, alpha, img2, 1 - alpha, 0)

        img2 = imr.resize(img2, height=plimg_h)         # does stop added white space, but resizes
#         print("new img shape ", img2.shape)
        # While space happens when h of new img is smaller then placeholder
    #     aoi_btn.configure(text="Add To AOI")   # works

        aoiImg = ImageTk.PhotoImage(Image.fromarray(img2))
        aoi_img.configure(image=aoiImg)
        aoi_img.image = aoiImg
        # extr.configure(bg=bgc, fg=fgc)   # doesn't stop added white space

    # aoi_img.pack(side="top", fill="both", expand=1, pady=80)

    # cv2.waitKey(0)
    # ----------------------------
    brk_loop = False

    cap.release()
    cv2.destroyAllWindows()

def clear_aoi():
    global aoi_img
    global p_list
    global img2
    global final_aoi
    global compiled_overlay
    global p_list_save
    aoiImg = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Rover_Cam/aoi_sml.png"))
#     aoiImg = ImageTk.PhotoImage(Image.fromarray(img2))
    aoi_img.configure(image=aoiImg)
    aoi_img.image = aoiImg

    p_list_save = p_list

    img2 = []
    final_aoi = []
    compiled_overlay = []
    p_list = []

    final_aoi = np.zeros((11, 2, 3), dtype=np.uint8)

def popup_about():
    # global bgc, fgc
    pop = Toplevel()
    pop.geometry("600x600")
    pop.wm_title("About")
    frame1 = Frame(pop, bg=bgc)
    frame1.pack(fill=BOTH, expand=1)
    # pop.configure(padx=50, pady=50)

    about_lab1 = ttk.Label(frame1, text="About",
                   font=("Liberation Sans", 26), background=bgc, foreground=fgc)
    about_lab1.pack(side=TOP, pady=40)

    about_lab2 = ttk.Label(frame1, text='Copyright (C) 2022 Brendan Murphy - All Rights Reserved'
                        '\nThis file is part of the Rover Cam project.\n\nSee Rover_Manual.odt',
                           font=("Liberation Sans", 12), wraplength=500, background=bgc, foreground=fgc)

    about_lab2.pack()

    about_btn = Button(frame1, height=1,
                width=10,
                text="Close",
                font=("Liberation Sans", 12),
                bg=btc, command=pop.destroy)
    about_btn.pack(side=BOTTOM, pady=(0, 40))

# ------------------------------

# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
# main_frame.place(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame, highlightthickness=0)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
# my_canvas.place(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
# my_scrollbar.place(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


# Make scrollable with mouse wheel
def scroll_up(event):
#     my_canvas.yview_scroll(-1*(event.delta//120), "units")   # for windows, //higher num make small scroll steps.. messes up
    my_canvas.yview_scroll(-1, "units")

def scroll_down(event):
    my_canvas.yview_scroll(1, "units")

my_canvas.bind_all("<Button-4>", scroll_up)
my_canvas.bind_all("<Button-5>", scroll_down)  # Button-5 and 4 for linux scroll


# From comments:
# I tried to use this (linux here) but couldnt make it work, until I noticed that - I wonder why - event.delta was
# always zero. Solved it by calling simply yview_scroll(direction,"units")

# -------- Menu Bar ---------

menubar = Menu(root)
# menubar.configure(bg="red")
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=select_file)
filemenu.add_command(label="Load", command=load_btn)
filemenu.add_command(label="Save", command=save_btn)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About", command=popup_about)
menubar.add_cascade(label="About", menu=helpmenu)

root.config(menu=menubar)


# Dark color scheme from: https://colorhunt.co/palette/040303461111a13333b3541e
# "#040303"
# "#461111"
# "#A13333"
# "#B3541E"

# bgc = "#040303"
# fgc = "#B3541E"
# btc = "#A13333"
# bgt = "#461111"  # bg text

# Vintage
# "#141E27"
# "#203239"
# "#E0DDAA"
# "#EEEDDE"

bgc = "#141E27"
# fgc = "#203239"
btc = "#E0DDAA"
bgt = "#393E46"  # bg text

# All time most popular from that site
# "#222831"  bgt
# "#393E46"  bgc
# "#00ADB5"  btn    , bg=btc)
# "#EEEEEE"  txt    , bg=bgc, fg=fgc)

# bgc = "#393E46"
fgc = "#EEEEEE"
# btc = "#00ADB5"
# bgt = "#222831"  # bg text


# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas, bg=bgc)    # for title

below1 = Frame(second_frame, bg=bgc)     # for main paragraph
below1.pack(side=BOTTOM, fill=BOTH)

below1b = Frame(below1, bg=bgc)       # used for top btn's
below1b.pack(side=BOTTOM, fill=BOTH)

below1c = Frame(below1b, bg=bgc)       # set time para
below1c.pack(side=BOTTOM, fill=BOTH)

below1d = Frame(below1c, bg=bgc)       # st time label and txt boxs
below1d.pack(side=BOTTOM, fill=BOTH)

below1e = Frame(below1d, bg=bgc)       # st under txt labels or put them on same a txt boxs?
below1e.pack(side=BOTTOM, fill=BOTH)

below1f = Frame(below1e, bg=bgc)       # run at boot-up option
below1f.pack(side=BOTTOM, fill=BOTH)

below2 = Frame(below1f, bg=bgc)         # for s1
below2.pack(side=BOTTOM, fill=BOTH)

below3 = Frame(below2, bg=bgc)
below3.pack(side=BOTTOM, fill=BOTH)

below3b = Frame(below3, bg=bgc)
below3b.pack(side=BOTTOM, fill=BOTH)

below3c = Frame(below3b, bg=bgc)
below3c.pack(side=BOTTOM, fill=BOTH)

below3d = Frame(below3c, bg=bgc)
below3d.pack(side=BOTTOM, fill=BOTH)

below3e = Frame(below3d, bg=bgc)
below3e.pack(side=BOTTOM, fill=BOTH)

below4 = Frame(below3e, bg=bgc)
below4.pack(side=BOTTOM, fill=BOTH)

below5 = Frame(below4, bg=bgc)
below5.pack(side=BOTTOM, fill=BOTH)

below6 = Frame(below5, bg=bgc)
below6.pack(side=BOTTOM, fill=BOTH)

below7 = Frame(below6, bg=bgc)
below7.pack(side=BOTTOM, fill=BOTH)

below8 = Frame(below7, bg=bgc)
below8.pack(side=BOTTOM, fill=BOTH)

below9 = Frame(below8, bg=bgc)
below9.pack(side=BOTTOM, fill=BOTH)

below10 = Frame(below9, bg=bgc)
below10.pack(side=BOTTOM, fill=BOTH)

below11 = Frame(below10, bg=bgc)
below11.pack(side=BOTTOM, fill=BOTH)

below12 = Frame(below11, bg=bgc)
below12.pack(side=BOTTOM, fill=BOTH)

below13 = Frame(below12, bg=bgc)
below13.pack(side=BOTTOM, fill=BOTH)

below14 = Frame(below13, bg=bgc)
below14.pack(side=BOTTOM, fill=BOTH)

below15 = Frame(below14, bg=bgc)
below15.pack(side=BOTTOM, fill=BOTH)

below16 = Frame(below15, bg=bgc)
below16.pack(side=BOTTOM, fill=BOTH)

below17 = Frame(below16, bg=bgc)
below17.pack(side=BOTTOM, fill=BOTH)

below18 = Frame(below17, bg=bgc)
below18.pack(side=BOTTOM, fill=BOTH)

below19 = Frame(below18, bg=bgc)
below19.pack(side=BOTTOM, fill=BOTH)

below20 = Frame(below19, bg=bgc)
below20.pack(side=BOTTOM, fill=BOTH)

below21 = Frame(below20, bg=bgc)
below21.pack(side=BOTTOM, fill=BOTH)

below22 = Frame(below21, bg=bgc)
below22.pack(side=BOTTOM, fill=BOTH)

below23 = Frame(below22, bg=bgc)
below23.pack(side=BOTTOM, fill=BOTH)

below24 = Frame(below23, bg=bgc)
below24.pack(side=BOTTOM, fill=BOTH)

below25 = Frame(below24, bg=bgc)
below25.pack(side=BOTTOM, fill=BOTH)

# below25b = Frame(below25, bg=bgc)
# below25b.pack(side=BOTTOM, fill=BOTH)
#
# below25c = Frame(below25b, bg=bgc)
# below25c.pack(side=BOTTOM, fill=BOTH)

below26 = Frame(below25, bg=bgc)
below26.pack(side=BOTTOM, fill=BOTH)

below27 = Frame(below26, bg=bgc)
below27.pack(side=BOTTOM, fill=BOTH)

below28 = Frame(below27, bg=bgc)
below28.pack(side=BOTTOM, fill=BOTH)

below28b = Frame(below28, bg=bgc)
below28b.pack(side=BOTTOM, fill=BOTH)

below28c = Frame(below28b, bg=bgc)
below28c.pack(side=BOTTOM, fill=BOTH)

below29 = Frame(below28c, bg=bgc)
below29.pack(side=BOTTOM, fill=BOTH)

below29b = Frame(below29, bg=bgc)
below29b.pack(side=BOTTOM, fill=BOTH)

below30 = Frame(below29b, bg=bgc)
below30.pack(side=BOTTOM, fill=BOTH)

below31 = Frame(below30, bg=bgc)
below31.pack(side=BOTTOM, fill=BOTH)

# # Not doing "test"
# below32 = Frame(below31, bg=bgc)
# below32.pack(side=BOTTOM, fill=BOTH)
#
# below33 = Frame(below32, bg=bgc)
# below33.pack(side=BOTTOM, fill=BOTH)
#
# below34 = Frame(below33, bg=bgc)
# below34.pack(side=BOTTOM, fill=BOTH)


# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

# ------------------------------
'''
Pack
padx, pady, ipadx and ipadx.
buttonE.pack(side='right', ipadx=20, padx=30)    ipadx is inside padding
buttonX.pack(fill='x')
listboxA.pack(fill='both', expand=1)

Grid
resultButton.grid(column=0, row=2, pady=10, sticky=tk.W)    sticky N W S or E

Place, by cords or 0-1
labelD.place(relx=0.5, rely=0.5)          labelA.place(x=0, y=0)

Getting and setting text input values must be in this order
func
button, and text input
packing

'''

# Setting name font
# s_font = tkFont.Font(family="Liberation Sans", size=12, weight="bold")

tog_on = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Rover_Cam/tog_on4.png"))
tog_off = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Rover_Cam/tog_off4.png"))

title = ttk.Label(second_frame, text="Rover Cam", font=("Liberation Sans", 24), background=bgc, foreground=fgc, wraplength=670, justify="center")

main_lab = ttk.Label(below1, text="Welcome to Rover Cam, change settings here. Refer to manual for instructions. All time "
                     "based settings are in seconds.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

load1 = Button(below1b, height=1,
                width=10,
                text="Load",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: load_btn())

save1 = Button(below1b, height=1,
                width=10,
                text="Save",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: save_btn())    # relief="flat",

st_par = ttk.Label(below1c, text="Rover Cam is designed to run without an internet connection, if accurate date stamps "
                    "are desired, the time will have to be set for each time the program starts. "
                    "Note: Will lose accuracy over long periods of time. Does not compensate for leap years, or "
                    "day light savings. "
                    "Aim for the time that the pi will be booted, plus 40-60s, for boot and program start. "
                                       ,
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

st_lab = Label(below1d, text="Set Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_txtyr = Text(below1d, height=1, width=4, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtmo = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtda = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txthr = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtmi = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtse = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

st_labyr = Label(below1e, text="year", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labmo = Label(below1e, text="mo", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labda = Label(below1e, text="da", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labhr = Label(below1e, text="hr", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labmi = Label(below1e, text="mi", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labse = Label(below1e, text="se", font=("Liberation Sans", 12), bg=bgc, fg=fgc)


boot_on = True
def boot_tog_event(e):
    global boot_on
    global sett
    if boot_on == False:
        boot_tog.config(image=tog_off, relief=FLAT)
        sett["run_at_system_boot"] = "N"
        boot_on = True
    else:
        boot_tog.config(image=tog_on, relief=FLAT)
        sett["run_at_system_boot"] = "Y"
        boot_on = False
#     print(sett["run_at_system_boot"])

picam_on = True
def picam_tog_event(e):
    global picam_on
    global sett
    if picam_on == False:
        picam_tog.config(image=tog_off, relief=FLAT)
        sett["use_pi_camera"] = "N"
        picam_on = True
    else:
        picam_tog.config(image=tog_on, relief=FLAT)
        sett["use_pi_camera"] = "Y"
        picam_on = False

boot_lab = Label(below1f, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
boot_tog = Label(below1f, bg=bgc, fg=fgc)
boot_tog.bind("<Button-1>", boot_tog_event)

#$$$$
picam_par = ttk.Label(below3b, text='''To use a UBS camera leave this setting off''',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
picam_lab = Label(below3c, text="Use Pi Camera", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_tog = Label(below3c, bg=bgc, fg=fgc)
picam_tog.bind("<Button-1>", picam_tog_event)


s1_par = ttk.Label(below2, text="When motion is detected, how long should video be recorded for? "
                   "If set to under 1 second, then images will be saved instead. If set to 0 every motion "
                   "frame will be saved. If set to 0.5 then one motion frame per half second will be saved, "
                   "assuming the camera is seeing continuous motion.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s1_lab = Label(below3, text="Clip Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s1_txt = Text(below3, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)   # undo=True, wrap=NONE



#$$$$
fps_par = ttk.Label(below3d, text='''Set the max frames per second. This is limited by processing power so actual FPS maybe
lower. If using a pi camera and clips are playing fast with shorter clip times then 
set "Clip Time", then try a lower FPS.''',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

fps_lab = Label(below3e, text="FPS", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
fps_txt = Text(below3e, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s2_par = ttk.Label(below4, text="Motion area size: a lower number here may cause false detections. "
                   "A higher number will only detect larger moving objects, or closer small objects. "
                   "Recommended 20 or higher.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s2_lab = Label(below5, text="Motion Area", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s2_txt = Text(below5, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s3_par = ttk.Label(below6, text="Motion sensitivity baseline: a lower number here will increase sensitivity. "
                            "Is simular to motion area, but is effected more by brightly lite environments. "
                            "If false detections are a problem, then motion area should be experimented with first. "
                            "4 is a good number here.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s3_lab = Label(below7, text="Motion Sens", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s3_txt = Text(below7, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s4_par = ttk.Label(below8, text="Mode 1 just records on motion.\n"
                                "Mode 2 records and preforms actions/audio on motion.\n"
                                "Mode 3 just preforms actions/audio on motion.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s4_lab = Label(below9, text="Mode", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s4_txt = Text(below9, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s5_par = ttk.Label(below10, text='Optionally play audio or python3 files on motion. '
            'Will play any and all .wav or .py files in "/home/pi/Desktop/Rover_Cam/audio" '
            'one after another in alphabetical order. '
            'This can be left on, will not fault out even if no files in location.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s5_lab = Label(below11, text="Play Audio", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
# s5_txt = Text(below11, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

play_audio = True
def audio_tog_event(e):
    global play_audio
    global sett
    if play_audio == False:
        audio_tog.config(image=tog_off, relief=FLAT)
        sett["play_audio"] = "N"
        play_audio = True
    else:
        audio_tog.config(image=tog_on, relief=FLAT)
        sett["play_audio"] = "Y"
        play_audio = False
#     print(sett["play_audio"])


# audio_lab = Label(below1f, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
audio_tog = Label(below11, bg=bgc, fg=fgc)
audio_tog.bind("<Button-1>", audio_tog_event)


s6_par = ttk.Label(below12, text="Delay Audio will delay the running of files, in the audio folder "
                    "starting from motion detection.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s6_lab = Label(below13, text="Delay Audio", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s6_txt = Text(below13, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s7_par = ttk.Label(below14, text="Optional disable button (blue). "
                "Will stop recording, all actions, and audio, and start them again when pressed at a later time. "
                "A simple code can be set here, consisting of number of presses in set time frame. "
                "Any more or less presses within time frame, and system will not disable. "
                "To re-enable, follow same procedure. "
                "This feature can be used even when inside of motion detection area, but be sure to add ~0.5s delays "
                "before actions or audio. ex. start with a1 off 0.5, and Delay Audio 0.5s more.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s7_lab = Label(below15, text="Use Disable Button", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
# s7_txt = Text(below15, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


use_disable = True
def disable_tog_event(e):
    global use_disable
    global sett
    if use_disable == False:
        disable_tog.config(image=tog_off, relief=FLAT)
        sett["use_disable_button"] = "N"
        use_disable = True
    else:
        disable_tog.config(image=tog_on, relief=FLAT)
        sett["use_disable_button"] = "Y"
        use_disable = False
#     print(sett["play_audio"])


# audio_lab = Label(below1f, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
disable_tog = Label(below15, bg=bgc, fg=fgc)
disable_tog.bind("<Button-1>", disable_tog_event)


s8_lab = Label(below17, text="Disable Button Presses", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s8_txt = Text(below17, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s9_lab = Label(below19, text="Disable Button Time Frame", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s9_txt = Text(below19, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s10_par = ttk.Label(below20, text='Disable the disable button for a time after a failed disable attempt. '
                    'This makes it harder if someone is trying to guess the disable code. '
                    'The disable button will not have effect until this time is up. '
                    'Each time a failed attempt is made a text file will be created in the clips folder, '
                    'or the storage device folder when running mode 3, to keep record. '
                    'To lock until the system is rebooted (or the power going out and coming back on) '
                    'enter "infinity" instead of a number.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s10_lab = Label(below21, text="Lock Disable Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s10_txt = Text(below21, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s11_par = ttk.Label(below22, text='This is a start delay for all the mode files. The files might take a few seconds to start, but this '
                    'will add extra delay. Is useful if operator is physically inside the camera view, while using buttons, '
                    'or will pass through the camera view when leaving the area. This will delay mode start, from boot, disabled state, '
                    'and mode select state.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s11_lab = Label(below23, text="Activation Delay", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s11_txt = Text(below23, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s12_par = ttk.Label(below24, text="Set camera index. If you don't know your camera index, try 0, 1, 2 etc.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s12_lab = Label(below25, text="Camera Index", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s12_txt = Text(below25, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


a_par = ttk.Label(below26, text='Here you can write your custom program that turns GPIO pins on and off. '
                  'These are referred to as "Actions", each Action controls a separate pin. '
                  'The number that comes after "on" or "off" is the time in seconds that it will remain in that state. '
                  'Enter "on" or "off", followed by a number of seconds to remain in that state, repeat on a new line. '
                  'Alternate state with each new line. Always start in "off" state, even if for zero seconds. '
                  'Decimal numbers accepted.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

a_lab1 = Label(below27, text="Action 1", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab2 = Label(below27, text="Action 2", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab3 = Label(below27, text="Action 3", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab4 = Label(below27, text="Action 4", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

a_txt1 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt2 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt3 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt4 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


a_lab5 = Label(below28b, text="Action 5", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab6 = Label(below28b, text="Action 6", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab7 = Label(below28b, text="Action 7", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab8 = Label(below28b, text="Action 8", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

a_txt5 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt6 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt7 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt8 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


load2 = Button(below29, height=1,
                width=10,
                text="Load",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: load_btn())

save2 = Button(below29, height=1,
                width=10,
                text="Save",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: save_btn())

# aoi ---------

aoi_par = ttk.Label(below29b, text='Select Area Of Interest (AOI). Click the "Select/Add To AOI" button to set. '
                    'Another window will pop-up where you can click and drag. A green rectangle will indicate the '
                    'area that will be the aoi. Have a camera plugged in with the proper index setting. If an aoi is '
                    'set then any motion in the area of the frame that is NOT included in the aoi, will not trigger '
                    'any actions, clip recording, or audio. To remove the aoi effect, clear the aoi, and save.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

aoi_img = Label(below30, bg=bgc, fg=fgc)

aoi_btn = Button(below31, height=1,
                width=18,
                text="Select/Add To AOI",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: select_aoi())

aoi_clear_btn = Button(below31, height=1,
                width=18,
                text="Clear AOI",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: clear_aoi())



# # ---- Not doing "test" ----
# test_par = ttk.Label(below32, text='Test your settings. This will launch a new window, clips will be saved. '
#                      'Right click on window to exit.',
#                  font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
#
# test_lab1 = Label(below33, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
# test_lab2 = Label(below33, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
# test_lab3 = Label(below33, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
#
# test_tog1 = Label(below33, bg=bgc, fg=fgc)
# test_tog1.bind("<Button-1>", show_all_motion)
#
# test_tog2 = Label(below33, bg=bgc, fg=fgc)
# test_tog2.bind("<Button-1>", show_detected_motion)
#
# test_tog3 = Label(below33, bg=bgc, fg=fgc)
# test_tog3.bind("<Button-1>", show_frame)
#
# test_btn = Button(below31, height=1,
#                 width=18,
#                 text="Save & Test",
#                 font=("Liberation Sans", 12),
#                 bg=btc,
#                 command=lambda: save_test_btn())

# # frame_image = ImageTk.PhotoImage(Image.fromarray(image))
# ao_im = ImageTk.PhotoImage(Image.open("aoi_sml.png"))  # make smaller, moded this to load all


# # load aoi
# ao_im = cv2.imread(path_usb + "/aoi.png")
# plimg_h = 240
# ao_im = imr.resize(ao_im, height=plimg_h)
# # ao_im = ImageTk.PhotoImage(Image.open(path_usb + "/aoi.png"))
# ao_im = ImageTk.PhotoImage(Image.fromarray(ao_im))
# if ao_im.height() == 11 and ao_im.width() ==2:
#     print("no aoi to load, using placeholder")
#     ao_im = ImageTk.PhotoImage(Image.open(path_usb + "/aoi_sml.png"))
#
# # plimg_h = ao_im.height()
#
# # ao_im = imr.resize(ao_im, height=plimg_h)
# print(ao_im.height(), ao_im.width())
# aoi_img.config(image=ao_im)
# aoi_img.image = ao_im


aoi_par.pack(side='left', padx=100, pady=10)
aoi_img.pack(side="top", fill="both", expand=1, pady=20)
aoi_btn.pack(side='left', padx=(190, 50), pady=(20, 110))
aoi_clear_btn.pack(side='left', padx=(50, 50), pady=(20, 110))
# ---------

# title.pack(side='left', padx=340, pady=(50, 20))
title.pack(fill="none", expand=True, pady=(60, 20))     # to center
main_lab.pack(side='left', padx=100, pady=10)

load1.pack(side='left', padx=(200, 0), pady=20)
save1.pack(side='right', padx=(0, 200), pady=20)


st_par.pack(side='left', padx=100, pady=10)
st_lab.pack(side='left', padx=(140, 0), pady=(10, 0))
st_txtyr.pack(side='left', padx=(110, 10), pady=(10, 0))
st_txtmo.pack(side='left', padx=10, pady=(10, 0))
st_txtda.pack(side='left', padx=10, pady=(10, 0))
st_txthr.pack(side='left', padx=10, pady=(10, 0))
st_txtmi.pack(side='left', padx=10, pady=(10, 0))
st_txtse.pack(side='left', padx=10, pady=(10, 0))

st_labyr.pack(side='left', padx=(320, 10), pady=(0, 10))
st_labmo.pack(side='left', padx=(15, 10), pady=(0, 10))
st_labda.pack(side='left', padx=10, pady=(0, 10))
st_labhr.pack(side='left', padx=(13, 16), pady=(0, 10))
st_labmi.pack(side='left', padx=(9, 14), pady=(0, 10))
st_labse.pack(side='left', padx=10, pady=(0, 10))

boot_lab.pack(side='left', padx=(140, 0), pady=10)
boot_tog.config(image=tog_off)
# tog_on_img.image = tog_on
boot_tog.pack(side='right', padx=(0, 500), pady=10)

picam_par.pack(side='left', padx=100, pady=10)
picam_lab.pack(side='left', padx=(140, 0), pady=10)
picam_tog.config(image=tog_off)
picam_tog.pack(side='right', padx=(0, 500), pady=10)

s1_par.pack(side='left', padx=100, pady=10)
s1_lab.pack(side='left', padx=(140, 0), pady=10)
s1_txt.pack(side='right', padx=(0, 440), pady=10)

fps_par.pack(side='left', padx=100, pady=10)
fps_lab.pack(side='left', padx=(140, 0), pady=10)
fps_txt.pack(side='right', padx=(0, 440), pady=10)

s2_par.pack(side='left', padx=100, pady=10)
s2_lab.pack(side='left', padx=(140, 0), pady=10)
s2_txt.pack(side='right', padx=(0, 440), pady=10)

s3_par.pack(side='left', padx=100, pady=10)
s3_lab.pack(side='left', padx=(140, 0), pady=10)
s3_txt.pack(side='right', padx=(0, 440), pady=10)

s4_par.pack(side='left', padx=100, pady=10)
s4_lab.pack(side='left', padx=(140, 0), pady=10)
s4_txt.pack(side='right', padx=(0, 440), pady=10)

s5_par.pack(side='left', padx=100, pady=10)
s5_lab.pack(side='left', padx=(140, 0), pady=10)
# s5_txt.pack(side='right', padx=(0, 440), pady=10)

# audio_lab.pack(side='left', padx=(140, 0), pady=10)
audio_tog.config(image=tog_off)
audio_tog.pack(side='right', padx=(0, 500), pady=10)

s6_par.pack(side='left', padx=100, pady=10)
s6_lab.pack(side='left', padx=(140, 0), pady=10)
s6_txt.pack(side='right', padx=(0, 440), pady=10)

s7_par.pack(side='left', padx=100, pady=10)
s7_lab.pack(side='left', padx=(140, 0), pady=10)
# s7_txt.pack(side='right', padx=(0, 440), pady=10)

disable_tog.config(image=tog_off)
disable_tog.pack(side='right', padx=(0, 500), pady=10)


# s8_par.pack(side='left', padx=100, pady=10)
s8_lab.pack(side='left', padx=(125, 0), pady=10)   # special cause long label
s8_txt.pack(side='right', padx=(0, 440), pady=10)

# s9_par.pack(side='left', padx=100, pady=10)
s9_lab.pack(side='left', padx=(100, 0), pady=10)    # special cause long label
s9_txt.pack(side='right', padx=(0, 440), pady=10)

s10_par.pack(side='left', padx=100, pady=10)
s10_lab.pack(side='left', padx=(140, 0), pady=10)
s10_txt.pack(side='right', padx=(0, 440), pady=10)

s11_par.pack(side='left', padx=100, pady=10)
s11_lab.pack(side='left', padx=(140, 0), pady=10)
s11_txt.pack(side='right', padx=(0, 440), pady=10)

s12_par.pack(side='left', padx=100, pady=10)
s12_lab.pack(side='left', padx=(140, 0), pady=10)
s12_txt.pack(side='right', padx=(0, 440), pady=10)


a_par.pack(side='left', padx=100, pady=(10, 20))

a_lab1.pack(side='left', padx=(180, 60), pady=0)
a_lab2.pack(side='left', padx=22, pady=0)
a_lab3.pack(side='left', padx=65, pady=0)
a_lab4.pack(side='left', padx=20, pady=0)

a_txt1.pack(side='left', padx=(160, 15), pady=10)
a_txt2.pack(side='left', padx=15, pady=10)
a_txt3.pack(side='left', padx=15, pady=10)
a_txt4.pack(side='left', padx=15, pady=10)


a_lab5.pack(side='left', padx=(180, 60), pady=(10,0))
a_lab6.pack(side='left', padx=22, pady=(10,0))
a_lab7.pack(side='left', padx=65, pady=(10,0))
a_lab8.pack(side='left', padx=20, pady=(10,0))

a_txt5.pack(side='left', padx=(160, 15), pady=10)
a_txt6.pack(side='left', padx=15, pady=10)
a_txt7.pack(side='left', padx=15, pady=10)
a_txt8.pack(side='left', padx=15, pady=10)


load2.pack(side='left', padx=(200, 0), pady=(20, 35))
# actions.pack(side='left', padx=(60, 0), pady=(20, 35))
save2.pack(side='right', padx=(0, 200), pady=(20, 35))


load_btn()      # start will all loaded

# mainloop()
root.mainloop()



