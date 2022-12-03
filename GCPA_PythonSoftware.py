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

# 1 rev = dist traveled is pitch of threaded rod

pitch = .8 # distance between threads in metric units (cm)
step_ang = 1.8 # degrees
steps_per_rev_x = 400 # number of steps to travel the distance equivalent to pitch
steps_per_rev_y = 400 # number of steps to travel the distance equivalent to pitch
steps_per_rev_z = 400

ROOT = tk.Tk()
ROOT.geometry('1000x1000')
ROOT.withdraw()
cal = 'Calibration' 
date = datetime.datetime.now().timestamp()
# In[2]:

usb = simpledialog.askstring(title="USB Port Name", prompt= "Welcome to the Lead Collimator Positioning System! \n\nPlease insert the name of or path to the USB port you are using. This can be found in the devices settings on a Windows OS (example 'COM3') \nor in the /dev directory on a Mac (example 'usbmodem1200') \n\nInput USB Port:")

# Establish a serial connection with Arduino
try:
    ser = serial.Serial(usb, 9600)
except:
    tkmb.showerror("Error!", "Try unplugging and replugging the Arduino cable! Then re-run this cell. \n\nIf that still results in an error, re-check your usb port name. \n\n If you need more help please refer to the user manual.")



# In[3]:

# the input dialog
ot = simpledialog.askstring(title="Orientation", prompt= "Are you in the vertical orientation, horizontal orientation, or would you like to transition from one to the other? \n\nInput 'H' for horizontal, 'V' for vertical, or 'T' for transition:")
if ot == 'H':
    ser.write(str.encode("xEND,,1"))
    time.sleep(10)
    ser.write(str.encode("yEND,,0"))
    time.sleep(10)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',1' 
    ser.write(str.encode(movehome))
    file = open(r'sourcepositions.txt', 'w+')
    
    tkmb.showinfo("Horizontal Position", "Welcome to the horizontal position! You are now in the xy plane. The collimator will move to the home postion. On the positioning apparatus, we have labeled these coordinates for easy understanding of the coordinate system! The x-axis is the direction that uses two stepper motors, the y-axis uses only one. \n \nNow you will enter the x and y position that you would like the collimator to go.")

    # specifying the plot size
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
    
    time.sleep(10)
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
        gran = 0.1 #cm
        move_x = (gran/pitch) * steps_per_rev_x 
        while(start_stepsx > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            inputmovex = 'y,' + str(move_x) + ',1' #string formation to send to Arduino to move x motor right to next region
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos += gran
            time.sleep(2)
    
    if (xloc < 0):
        xloc = -xloc
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        gran = 0.1 #cm
        move_x = (gran/pitch) * steps_per_rev_x 
        while(start_stepsx > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
            inputmovex = 'y,' + str(move_x) + ',0' #string formation to send to Arduino to move x motor right to next region
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos -= gran
            time.sleep(2)
            
    start_stepsy = (yloc/pitch) * steps_per_rev_y
    gran = 0.1 #cm
    move_y = (gran/pitch) * steps_per_rev_y
    while(start_stepsy > 0):
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
        inputmovey = 'x,' + str(move_y) + ',0' #string formation to send to Arduino to move x motor right to next region
        ser.write(str.encode(inputmovey))
        start_stepsy -= move_y
        y_pos += gran
        time.sleep(2)
        
    move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the horizontal mode? Yes or No"))
    while (move == "yes" or move == "Yes" or move == "y"):
        
           xloc = int(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           while (xloc)>20 or (xloc)<-20: 
                xloc = int(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           
           yloc = int(simpledialog.askstring(title="y position", prompt= "Input the y-position that you would like the collimator to move (between 0 and 20 cm)"))
           while (yloc)>20 or (yloc)<0: 
                yloc = int(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid y position. \nInput the y-position that you would like the collimator to move (between 0 and 20 cm)"))
           
           x_move = xloc - x_pos
           
           if (x_move > 0):
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovex = 'y,' + str(move_x) + ',1' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos += gran
                time.sleep(2)
           if (x_move < 0):
            x_move = -x_move
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovex = 'y,' + str(move_x) + ',0' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos -= gran
                time.sleep(2)
           
           y_move = yloc - y_pos
           
           if (y_move > 0):
            start_stepsy = (y_move/pitch) * steps_per_rev_z
            while(start_stepsy > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovey = 'x,' + str(move_y) + ',0' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovey))
                start_stepsy -= move_y
                y_pos += gran
                time.sleep(2)
           if (y_move < 0):
            y_move = -y_move
            start_stepsz = (y_move/pitch) * steps_per_rev_x
            while(start_stepsy > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , y_pos))
                inputmovey = 'x,' + str(move_y) + ',1' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovey))
                start_stepsy -= move_y
                y_pos += gran
                time.sleep(2)
           
           move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the horizontal mode? Yes or No")) 
    
    file.close()
    
if ot == 'V':
    ser.write(str.encode("xEND,,1"))
    time.sleep(10)
    ser.write(str.encode("yEND,,1"))
    time.sleep(10)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',0' 
   
    file = open(r'sourcepositions.txt', 'w+')
   
    tkmb.showinfo("Vertical Position", "Welcome to the vertical position! You are now in the xz plane. The collimator will move to the home postion. On the positioning apparatus, we have labeled these coordinates for easy understanding of the coordinate system! The z-axis is up and down, the x-axis side to side. \n \nNow you will enter the x and z position that you would like the collimator to go.")
    # specifying the plot size
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
    time.sleep(10)
    
    xloc = int(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    while (xloc)>20 or (xloc)<-20: 
         xloc = int(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
    
    zloc = int(simpledialog.askstring(title="z position", prompt= "Input the z-position that you would like the collimator to move (between 0 and 20 cm)"))
    while (zloc)>20 or (zloc)<0: 
         zloc = int(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid z position. \nInput the z-position that you would like the collimator to move (between 0 and 20 cm)"))
   
    x_pos = 0
    z_pos = 0
    
    if (xloc > 0):
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        gran = 0.1 #cm
        move_x = (gran/pitch) * steps_per_rev_x
        while(start_stepsx > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            inputmovex = 'y,' + str(move_x) + ',1' #string formation to send to Arduino to move x motor right to next region
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos += gran
            time.sleep(2)
    
    if (xloc < 0):
        xloc = -xloc
        start_stepsx = (xloc/pitch) * steps_per_rev_x
        gran = 0.1 #cm
        move_x = (gran/pitch) * steps_per_rev_x 
        while(start_stepsx > 0):
            date = datetime.datetime.now().timestamp()
            file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
            inputmovex = 'y,' + str(move_x) + ',0' #string formation to send to Arduino to move x motor right to next region
            ser.write(str.encode(inputmovex))
            start_stepsx -= move_x
            x_pos -= gran
            time.sleep(2)
    
    tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are hooked on the aparratus! you are about to move the collimator up!")
    start_stepsz = (zloc/pitch) * steps_per_rev_y
    
    gran = 0.1 #cm
    move_z = (gran/pitch) * steps_per_rev_y
    
    while(start_stepsz > 0):
        date = datetime.datetime.now().timestamp()
        file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
        inputmovez = 'x,' + str(move_z) + ',0' #string formation to send to Arduino to move x motor right to next region
        ser.write(str.encode(inputmovez))
        start_stepsz -= move_z
        z_pos += gran
        time.sleep(2)
        
    move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the vertical mode? Yes or No"))
    while (move == "yes" or move == "Yes" or move == "yes"):
        
           xloc = int(simpledialog.askstring(title="x position", prompt= "Input the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           while (xloc)>20 or (xloc)<-20: 
                xloc = int(simpledialog.askstring(title="x position", prompt= "Oops! Please enter a valid x position. \nInput the x-position that you would like the collimator to move (between -20 and 20 cm)"))
           
           zloc = int(simpledialog.askstring(title="z position", prompt= "Input the z-position that you would like the collimator to move (between 0 and 20 cm)"))
           while (zloc)>20 or (zloc)<0: 
                zloc = int(simpledialog.askstring(title="y position", prompt= "Oops! Please enter a valid z position. \nInput the z-position that you would like the collimator to move (between 0 and 20 cm)"))
           
           x_move = xloc - x_pos
           
           if (x_move > 0):
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                inputmovex = 'y,' + str(move_x) + ',1' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos += gran
                time.sleep(2)
           if (x_move < 0):
            x_move = -x_move
            start_stepsx = (x_move/pitch) * steps_per_rev_x
            while(start_stepsx > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                inputmovex = 'y,' + str(move_x) + ',0' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovex))
                start_stepsx -= move_x
                x_pos -= gran
                time.sleep(2)
           
           z_move = zloc - z_pos
           
           if (z_move > 0):
            tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are hooked on the aparratus! you are about to move the collimator up!")
            start_stepsz = (z_move/pitch) * steps_per_rev_z
            while(start_stepsz > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                inputmovez = 'x,' + str(move_z) + ',0' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovez))
                start_stepsz -= move_z
                z_pos += gran
                time.sleep(2)
           if (z_move < 0):
            tkmb.showwarning("Weights", "WARNING: Please make sure the additional weights are NOT hooked on the aparratus! you are about to move the collimator down!")
            z_move = -z_move
            start_stepsz = (z_move/pitch) * steps_per_rev_x
            while(start_stepsz > 0):
                date = datetime.datetime.now().timestamp()
                file.write("%5.2f %5.2f %5.2f\n" % (date, x_pos , z_pos))
                inputmovez = 'x,' + str(move_z) + ',1' #string formation to send to Arduino to move x motor right to next region
                ser.write(str.encode(inputmovez))
                start_stepsz -= move_z
                z_pos += gran
                time.sleep(2)
           
           move = str(simpledialog.askstring(title="Move again?", prompt= "Would you like to move to another position in the vertical mode? Yes or No"))
           
    file.close() 
if ot == 'T':
    tkmb.showinfo("Transition Position", "Welcome to the transition position! The collimator will move to the home (transition) position, and then you may rotate the apparatus. \n\nIf you are transitioning from the horizontal to vertical position, rotate the apparatus and attach the counterweights and support blocks in the mount. \n\nIf you are transitioning from the vertical to horizontal position, remove the counterweights, ropes, and support blocks in the mount and then rotate the apparatus. \n\nFinally, re-run this cell and pick which plane you would like to move in! :)")
    ser.write(str.encode("xEND,,1"))
    time.sleep(2)
    ser.write(str.encode("yEND,,1"))
    time.sleep(2)
    start = (20/pitch) * steps_per_rev_x
    movehome = 'y,' + str(start) + ',0' 
    ser.write(str.encode(movehome))

