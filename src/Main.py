import tkinter
from threading import Thread,Event
from subprocess import Popen
from tkinter.constants import LEFT, X
from PIL import Image, ImageTk
from tkinter.ttk import *
import tkinter.font as font
import cv2
from numpy.lib.function_base import place

top = tkinter.Tk()
top.geometry('500x645+500+70')
myFont = font.Font(family='Arial Rounded MT Bold', size=10)
label1 = tkinter.Label(top, text="AI/ML for Anomalous Surveillance:\n A Detection and Alert System", bg='#3d3d3d', fg='white', font='arial 15 bold').place(x=90,y=75)

class Controller(object):
    def __init__(self):
        self.thread1 = None
        self.stop_threads = Event()

#====================================================== Weapon Detection ======================================================

    def weapon(self):
        term1 = Popen(["./lib/env/thesis_env/python", "./src/weapon-detection.py"])
        weaponWindow = tkinter.Tk()
        weaponWindow.geometry('825x715+360+65')
        weaponWindow['background']='#3d3d3d'
        weaponWindow.overrideredirect(1)

        def closeweapon():
            weaponWindow.destroy()
            term1.terminate()

        wpclosebtn = tkinter.Button(weaponWindow, height=3, width=33, fg='white', bg='#3d3d3d', text = "CHANGE SYSTEM", font='arial 9 bold', command = closeweapon, activebackground='#3d3d3d')
        wpclosebtn.place(x=293, y=635)

#====================================================== Drowsiness Detection ======================================================

    def drowsiness(self):
        global term1
        term1 = Popen (["./lib/env/drowsiness_env/python", "./src/drowsiness-detection.py"])
        drowsinessWindow = tkinter.Tk()
        drowsinessWindow.geometry('825x715+360+65')
        drowsinessWindow['background']='#3d3d3d'
        drowsinessWindow.overrideredirect(1)

        def closedrowsiness():
            drowsinessWindow.destroy()
            term1.terminate()

        wpclosebtn = tkinter.Button(drowsinessWindow, height=3, width=33, fg='white', bg='#3d3d3d', text = "CHANGE SYSTEM", font='arial 9 bold', command = closedrowsiness, activebackground='#3d3d3d')
        wpclosebtn.place(x=293, y=635)

#====================================================== Violence Detection ======================================================

    def violence(self):
        #term1 = Popen (["./env/thesis_env/python", "DeployLive.py"])
        term1 = Popen (["./lib/env/thesis_env/python", "./src/violence-detection.py"])
        violenceWindow = tkinter.Tk()
        violenceWindow.geometry('825x715+360+65')
        violenceWindow['background']='#3d3d3d'
        violenceWindow.overrideredirect(1)

        def closeviolence():
            violenceWindow.destroy()
            term1.terminate()

        wpclosebtn = tkinter.Button(violenceWindow, height=3, width=33, fg='white', bg='#3d3d3d', text = "CHANGE SYSTEM", font='arial 9 bold', command = closeviolence, activebackground='#3d3d3d')
        wpclosebtn.place(x=293, y=635)

#====================================================== Fall Detection ======================================================

    def fall(self):
        global term1
        term1 = Popen (["./lib/env/thesis_env/python", "./src/fall-detection.py"])
        fallWindow = tkinter.Tk()
        fallWindow.geometry('825x715+360+65')
        fallWindow['background']='#3d3d3d'
        fallWindow.overrideredirect(1)

        def closefall():
            fallWindow.destroy()
            term1.terminate()

        wpclosebtn = tkinter.Button(fallWindow, height=3, width=33, fg='white', bg='#3d3d3d', text = "CHANGE SYSTEM", font='arial 9 bold', command = closefall, activebackground='#3d3d3d')
        wpclosebtn.place(x=293, y=635)

    def exit(self):
        top.destroy()
        
#====================================================== Buttons ======================================================
    
control = Controller()

BtnC = tkinter.Button(top, height=4, width=40, fg='white', bg='#3d3d3d', anchor='center', padx=25,   text = "        WEAPON DETECTION", font=myFont, command = control.weapon, activebackground='#3d3d3d')
BtnC.place(x=65, y=185)

BtnD = tkinter.Button(top, height=4, width=40, fg='white', bg='#3d3d3d', anchor='center', padx=25,   text = "        DROWSINESS DETECTION", font=myFont, command = control.drowsiness, activebackground='#3d3d3d')
BtnD.place(x=65, y=275)

BtnE = tkinter.Button(top, height=4, width=40, fg='white', bg='#3d3d3d', anchor='center', padx=25,   text = "        FALLING DETECTION", font=myFont, command = control.fall, activebackground='#3d3d3d')
BtnE.place(x=65, y=455)

BtnF = tkinter.Button(top, height=4, width=40, fg='white', bg='#3d3d3d', anchor='center', padx=25,   text = "        VIOLENCE DETECTION", font=myFont, command = control.violence, activebackground='#3d3d3d')
BtnF.place(x=65, y=365)

exit = tkinter.Button(top, height=1, width=3, text = "X", bg='white', bd=0, font=myFont, command = control.exit)
exit.place(x=465, y=5)

#====================================================== Images/Icons Import ======================================================

#my_pic = Image.open("./Icons/IMGedit.png")
iconA = Image.open("./src/index/Wcamera.png")
iconAa = Image.open("./src/index/Wcamera.png")
iconAb = Image.open("./src/index/Wcamera.png")
iconAc = Image.open("./src/index/Wcamera.png")


#resized = my_pic.resize((776, 589))
resizediconA = iconA.resize((35, 35))
resizediconAa = iconAa.resize((35, 35))
resizediconAb = iconAb.resize((35, 35))
resizediconAc = iconAc.resize((35, 35))
#resizediconB = iconB.resize((35, 35))

#new_pic = ImageTk.PhotoImage(resized)
iconA = ImageTk.PhotoImage(resizediconA)
iconAa = ImageTk.PhotoImage(resizediconAa)
iconAb = ImageTk.PhotoImage(resizediconAb)
iconAc = ImageTk.PhotoImage(resizediconAc)
#iconB = ImageTk.PhotoImage(resizediconB)

#my_label = tkinter.Label(top, image=new_pic, borderwidth=0)
my_iconA = tkinter.Label(top, image=iconA, borderwidth=0, bg='#3d3d3d')
my_iconAa = tkinter.Label(top, image=iconAa, borderwidth=0, bg='#3d3d3d')
my_iconAb = tkinter.Label(top, image=iconAb, borderwidth=0, bg='#3d3d3d')
my_iconAc = tkinter.Label(top, image=iconAc, borderwidth=0, bg='#3d3d3d')
#my_iconB = tkinter.Label(top, image=iconB, borderwidth=0, bg='#3d3d3d')

#my_label.place(x=323,y=55)
my_iconA.place(x=100,y=200)
my_iconAa.place(x=100,y=290)
my_iconAb.place(x=100,y=380)
my_iconAc.place(x=100,y=470)
#my_iconB.place(x=125,y=410)

top['background']='#3d3d3d'
top.overrideredirect(1)
top.mainloop()