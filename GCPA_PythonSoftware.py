# -*- coding: utf-8 -*-
"""
Green's Goblins Senior Design Code

Goblin's Collimator Positioning Apparatus 

Fall 2022

@author: Anna Taylor, Ben Clark, Annalise Wolfe 
"""

# In[1]:
import numpy as np
import matplotlib.pyplot as py
import time
import serial
import datetime
import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as tkmb

#Constants related to the Arduino, stepper motors,and the default granularity and wait time 
pitch = .8 # distance between threads in metric units (cm)
step_ang = 1.8 # degrees
steps_per_rev_x = 400 # number of steps to travel the distance equivalent to pitch
steps_per_rev_y = 400 # number of steps to travel the distance equivalent to pitch
steps_per_rev_z = 400 # number of steps to travel the distance equivalent to pitch
gran = 0.1 # the default step size taken to get to a coordinate (in cm)
wait_time = 2 # the default wait times taken in between steos to get to a coordinate (in cm)
ROOT = tk.Tk()
ROOT.geometry('1000x1000')
ROOT.withdraw()
date = datetime.datetime.now().timestamp()
# In[2]:
#Prompt for the user to put in the name and/or path to the USB connection
usb = simpledialog.askstring(title="USB Port Name", prompt= "Welcome to the Lead Collimator Positioning System! \n\nPlease insert the name of or path to the USB port you are using. This can be found in the devices settings on a Windows OS (example 'COM3') \nor in the /dev directory on a Mac (example 'usbmodem1200') \n\nInput USB Port:")

# Establish a serial connection with Arduino
try:
    ser = serial.Serial(usb, 9600)
except:
    tkmb.showerror("Error!", "Try unplugging and replugging the Arduino cable! Then re-run this cell.  \n\nIf that still results in an error, re-check your usb port name. \n\n If you need more help please refer to the user manual.")
# In[3]:

# Choosing which mode the user wants to be in
ot = simpledialog.askstring(title="Orientation", prompt= "Are you in the vertical orientation, horizontal mode, or would you like to transition from one to the other? \n\nInput 'H' for horizontal, 'V' for vertical, or 'T' for transition:")
if ot == 'H' or ot =='h':
    
    #Moving to home (0,0) position
    ser.write(str.encode("xEND,,1"))
    time.sleep(20)
    ser.write(str.encode("yEND,,1"))
    time.sleep(30)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',0' 
    ser.write(str.encode(movehome))
    time.sleep(20)
    file = open(r'sourpositions.txt', 'w+')
    tkmb.showinfo("Horizontal Position", "Welcome to the horizontal position! You are now in the xy plane. The collimator will move to the home postion. On the positioning apparatus, we have labeled these coordinates for easy understanding of the coordinate system! The x-axis is the direction that uses two stepper motors, the y-axis uses only one. \n \nNow you will enter the x and y position that you would like the collimator to go.")

    # Visualization of Coordinate System
    py.figure(figsize = (10, 5))
    u=0.     #x-position of the center
    v=1.5    #y-position of the center
    a=3.5     #radius on the x-axis
    b=1.5    #radius on the y-axis
    x = np.linspace(-20, 20, 100)
    py.plot( u+a*np.cos(x) , v+b*np.sin(x) , color = 'gray')
    py.axvline(x = 0, color = 'black')
    py.fill_between(u+a*np.cos(x) , v+b*np.sin(x) , alpha=1, color ='gray', label = "collimator in home (0,0) position")
    py.ylim(0,20)
    py.xlim(-20,20)
    py.legend()
    py.xlabel("x-axis (cm), with x = 0 in the middle of the apparatus")
    py.ylabel("y-axis (cm)")
    py.title("visualization of the x-y (horizontal) plane of movement (bird-eye view)")
    py.show()
    
    #Asking which position on the coordinate system the user wants the collimator to move to 
    xloc = float(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    while (xloc)>20 or (xloc)<-20: 
         xloc = float(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    
    yloc = float(simpledialog.askstring(title="y position", prompt= "Input the y-position that you would like the collimator to move (between 0 and 20 cm)"))
    while (yloc)>20 or (yloc)<0: 
         yloc = float(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid y position. \nInput the y-position that you would like the collimator to move (between 0 and 20 cm)"))
    
    x_pos = 0
    y_pos = 0
    
    if (xloc > 0):
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        move_x = (gran/pitch) * steps_per_rev_x 
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
        while(start_stepsx >= move_x):
            inputmovex = 'y,' + str(move_x) + ',1' 
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos += gran
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            time.sleep(wait_time)
        if start_stepsx != 0:
            temp = xloc % gran
            move_extra = start_stepsx 
            inputmoveextra = 'y,' + str(move_extra) + ',1'
            ser.write(str.encode(inputmoveextra))
            x_pos += temp
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            time.sleep(wait_time)
            
    if (xloc < 0):
        xloc = -xloc
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
        move_x = (gran/pitch) * steps_per_rev_x 
        while(start_stepsx >= move_x):
            inputmovex = 'y,' + str(move_x) + ',0' 
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos -= gran
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            time.sleep(wait_time)
        if start_stepsx != 0:
            temp = xloc % gran
            move_extra = start_stepsx 
            inputmoveextra = 'y,' + str(move_extra) + ',0'
            ser.write(str.encode(inputmoveextra))
            x_pos -= temp
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            time.sleep(wait_time)
            
    start_stepsy = (yloc/pitch) * steps_per_rev_y
    date = datetime.datetime.now().timestamp()
    file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
    move_y = (gran/pitch) * steps_per_rev_y
    while(start_stepsy >= move_y):
        inputmovey = 'x,' + str(move_y) + ',0' 
        ser.write(str.encode(inputmovey))
        start_stepsy -= move_y
        y_pos += gran
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
        time.sleep(wait_time)
    if start_stepsy != 0:
        temp = yloc % gran
        move_extra = start_stepsy 
        inputmoveextra = 'x,' + str(move_extra) + ',0'
        ser.write(str.encode(inputmoveextra))
        y_pos += temp
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
        time.sleep(wait_time)
   
    # Asking if the user wants the collimator to move to a new position    
    move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the horizontal mode? Yes or No"))
    while (move == "yes" or move == "Yes" or move == "y"):
        
           xloc = float(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           while (xloc)>20 or (xloc)<-20: 
                xloc = float(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           
           yloc = float(simpledialog.askstring(title="y position", prompt= "Input the y-position that you would like the collimator to move (between 0 and 20 cm)"))
           while (yloc)>20 or (yloc)<0: 
                yloc = float(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid y position. \nInput the y-position that you would like the collimator to move (between 0 and 20 cm)"))
           
           x_move = xloc - x_pos
           if (x_move > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx >= move_x):
                inputmovex = 'y,' + str(move_x) + ',1' 
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos += gran
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                time.sleep(wait_time)
            if start_stepsx != 0:
                temp = xloc % gran
                move_extra = start_stepsx 
                inputmoveextra = 'y,' + str(move_extra) + ',1'
                ser.write(str.encode(inputmoveextra))
                x_pos += temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                time.sleep(wait_time)
           if (x_move < 0):
            x_move = -x_move
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx >= move_x):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovex = 'y,' + str(move_x) + ',0' 
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos -= gran
                time.sleep(wait_time)
            if start_stepsx != 0:
                temp = xloc % gran
                move_extra = start_stepsx 
                inputmoveextra = 'y,' + str(move_extra) + ',0'
                ser.write(str.encode(inputmoveextra))
                x_pos -= temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                time.sleep(wait_time)
           
           y_move = yloc - y_pos
           
           if (y_move > 0):
            start_stepsy = (y_move/pitch) * steps_per_rev_z
            while(start_stepsy >= move_y):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovey = 'x,' + str(move_y) + ',0' 
                ser.write(str.encode(inputmovey))
                start_stepsy -= move_y
                y_pos += gran
                time.sleep(wait_time)
            if start_stepsy != 0:
                temp = yloc % gran
                move_extra = start_stepsy 
                inputmoveextra = 'x,' + str(move_extra) + ',0'
                ser.write(str.encode(inputmoveextra))
                y_pos += temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                time.sleep(wait_time)
           if (y_move < 0):
            y_move = -y_move
            start_stepsz = (y_move/pitch) * steps_per_rev_x
            while(start_stepsy >= move_y):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovey = 'x,' + str(move_y) + ',1' 
                ser.write(str.encode(inputmovey))
                start_stepsy -= move_y
                y_pos += gran
                time.sleep(wait_time)
            if start_stepsy != 0:
                temp = yloc % gran
                move_extra = start_stepsy 
                inputmoveextra = 'x,' + str(move_extra) + ',1'
                ser.write(str.encode(inputmoveextra))
                y_pos -= temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                time.sleep(wait_time)
                
           move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the horizontal mode? Yes or No")) 
    
    file.close()
    
if ot == 'V' or ot == 'v':
    #Moving to home (0,0) position
    tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are NOT hooked on the apparatus! You are about to move the collimator down!")
    time.sleep(1)
    ser.write(str.encode("xEND,,1"))
    time.sleep(20)
    ser.write(str.encode("yEND,,1"))
    time.sleep(30)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',0' 
    ser.write(str.encode(movehome))
    file = open(r'sourcepositions.txt', 'w+')
    tkmb.showinfo("Vertical Position", "Welcome to the vertical position! You are now in the xz plane. The collimator will move to the home postion. On the positioning apparatus, we have labeled these coordinates for easy understanding of the coordinate system! The z-axis is up and down, the x-axis side to side. \n \nNow you will enter the x and z position that you would like the collimator to go.")
    
    # Visualization of Coordinate System
    py.figure(figsize = (10, 5))
    u=0.     #x-position of the center
    v=1.5    #y-position of the center
    a=3.5   #radius on the x-axis
    b=1.5    #radius on the y-axis
    x = np.linspace(-20, 20, 100)
    py.plot( u+a*np.cos(x) , v+b*np.sin(x) , color = 'gray')
    py.axvline(x = 0, color = 'black')
    py.fill_between(u+a*np.cos(x) , v+b*np.sin(x) , alpha=1, color ='gray', label = "collimator in home (0,0) position")
    py.ylim(0,20)
    py.xlim(-20,20)
    py.legend()
    py.xlabel("x-axis, with x = 0 in the middle of the apparatus")
    py.ylabel("z-axis, with z = 0 at the bottom of the apparatus")
    py.title("visualization of the x-z (vertical) plane of movement")
    py.show()
    
    #Asking which position on the coordinate system the user wants the collimator to move to 
    xloc = float(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    while (xloc)>20 or (xloc)<-20: 
         xloc = float(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    
    zloc = float(simpledialog.askstring(title="z position", prompt= "Input the z-position that you would like the collimator to move (between 0 and 20 cm)"))
    while (zloc)>20 or (zloc)<0: 
         zloc = float(simpledialog.askstring(title="z position", prompt= "Oops! Please enter a valid z position. \nInput the z-position that you would like the collimator to move (between 0 and 20 cm)"))
    
    x_pos = 0
    z_pos = 0
    
    if (xloc > 0):
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        move_x = (gran/pitch) * steps_per_rev_x 
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
        while(start_stepsx >= move_x):
            inputmovex = 'y,' + str(move_x) + ',1' 
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos += gran
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            time.sleep(wait_time)
        if start_stepsx != 0:
            temp = xloc % gran
            move_extra = start_stepsx 
            inputmoveextra = 'y,' + str(move_extra) + ',1'
            ser.write(str.encode(inputmoveextra))
            x_pos += temp
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            time.sleep(wait_time)
            
    if (xloc < 0):
        xloc = -xloc
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
        move_x = (gran/pitch) * steps_per_rev_x 
        while(start_stepsx >= move_x):
            inputmovex = 'y,' + str(move_x) + ',0' 
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos -= gran
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            time.sleep(wait_time)
        if start_stepsx != 0:
            temp = xloc % gran
            move_extra = start_stepsx 
            inputmoveextra = 'y,' + str(move_extra) + ',0'
            ser.write(str.encode(inputmoveextra))
            x_pos -= temp
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            time.sleep(wait_time)
    
    start_stepsz = (zloc/pitch) * steps_per_rev_y
    move_z = (gran/pitch) * steps_per_rev_y
    
    if (zloc!=0):
        tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are hooked on the apparatus! You are about to move the collimator up!")
    
    date = datetime.datetime.now().timestamp()
    file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
    while(start_stepsz >= move_z):
        inputmovez = 'x,' + str(move_z) + ',0' 
        ser.write(str.encode(inputmovez))
        start_stepsz -= move_z
        z_pos += gran
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
        time.sleep(wait_time)
    if start_stepsz != 0:
        temp = zloc % gran
        move_extra = start_stepsz
        inputmoveextra = 'x,' + str(move_extra) + ',0'
        ser.write(str.encode(inputmoveextra))
        z_pos += temp
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
        time.sleep(wait_time)
    
    # Asking if the user wants the collimator to move to a new position       
    move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the vertical mode? Yes or No"))
    while (move == "yes" or move == "Yes" or move == "yes"):
        
           xloc = float(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           while (xloc)>20 or (xloc)<-20: 
                xloc = float(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           
           zloc = float(simpledialog.askstring(title="z position", prompt= "Input the z-position that you would like the collimator to move (between 0 and 20 cm)"))
           while (zloc)>20 or (zloc)<0: 
                zloc = float(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid z position. \nInput the z-position that you would like the collimator to move (between 0 and 20 cm)"))
           
           x_move = xloc - x_pos
           if (x_move > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx >= move_x):
                inputmovex = 'y,' + str(move_x) + ',1' 
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos += gran
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
            if start_stepsx != 0:
                temp = xloc % gran
                move_extra = start_stepsx 
                inputmoveextra = 'y,' + str(move_extra) + ',1'
                ser.write(str.encode(inputmoveextra))
                x_pos += temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
           if (x_move < 0):
            x_move = -x_move
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx >= move_x):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                inputmovex = 'y,' + str(move_x) + ',0' 
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos -= gran
                time.sleep(wait_time)
            if start_stepsx != 0:
                temp = xloc % gran
                move_extra = start_stepsx 
                inputmoveextra = 'y,' + str(move_extra) + ',0'
                ser.write(str.encode(inputmoveextra))
                x_pos -= temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
           
           z_move = zloc - z_pos
           
           if (z_move > 0):
            tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are hooked on the apparatus! You are about to move the collimator up!")
            start_stepsz = (z_move/pitch) * steps_per_rev_z
            while(start_stepsz >= move_z):
                inputmovez = 'x,' + str(move_z) + ',0' 
                ser.write(str.encode(inputmovez))
                start_stepsz -= move_z
                z_pos += gran
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
            if start_stepsz != 0:
                temp = zloc % gran
                move_extra = start_stepsz
                inputmoveextra = 'x,' + str(move_extra) + ',0'
                ser.write(str.encode(inputmoveextra))
                z_pos += temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
           if (z_move < 0):
            tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are NOT hooked on the apparatus! You are about to move the collimator down!")
            z_move = -z_move
            start_stepsz = (z_move/pitch) * steps_per_rev_x
            while(start_stepsz >= move_z):
                inputmovez = 'x,' + str(move_z) + ',1' 
                ser.write(str.encode(inputmovez))
                start_stepsz -= move_z
                z_pos -= gran
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
            if start_stepsz != 0:
                temp = zloc % gran
                move_extra = start_stepsz
                inputmoveextra = 'x' + str(move_extra) + ',1'
                ser.write(str.encode(inputmoveextra))
                z_pos -= temp
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                time.sleep(wait_time)
           
           move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the vertical mode? Yes or No"))
           
    file.close() 

if ot == 'T' or ot =='t':
    tkmb.showinfo("Transition Position", "Welcome to the transition position! The collimator will move to the home (transition) position, and then you may rotate the apparatus. \n\nIf you are transitioning from the horizontal to vertical position, rotate the apparatus and attach the counterweights and support blocks in the mount. \n\nIf you are transitioning from the vertical to horizontal position, remove the counterweights, ropes, and support blocks in the mount and then rotate the apparatus.\n\nFinally, re-run this cell and pick which plane you would like to move in! :)")
    tkmb.showwarning("Weights", "WARNING: If transitioning from vertical to horizontal please make sure the additional weights are NOT hooked on the apparatus! You are about to move the collimator down!")
    time.sleep(5)
    # Moving to the home (0,0) position
    ser.write(str.encode("xEND,,1"))
    time.sleep(20)
    ser.write(str.encode("yEND,,1"))
    time.sleep(30)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',0' 
    ser.write(str.encode(movehome))
    
