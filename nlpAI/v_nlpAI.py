#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
from tkinter import *

from tkinter import messagebox

class view():
  def __init__(self): #setup everything without controller callbacks
    #layout the frames in the top window
    self.top = Tk()
    self.grp = Frame(self.top) #put a group subframe for stats and email at the top of window
    self.grp.pack(side=TOP)


######################## Stats Subframe #################################
    self.stats = Frame(self.grp) #fill the left side of the grp subframe with a statistics frame
    self.stats.pack(side=LEFT,fill=Y)

    self.trainCtLbl = Label(self.stats, text = 'trainCt')
    self.trainCtLbl.pack(side=TOP)

    self.trainCt = StringVar()
    self.trainCtDat = Label(self.stats, textvariable = self.trainCt, relief = RAISED )

    self.trainCt.set("430")
    self.trainCtDat.pack(side=TOP)


################# Email Reader Subframe ################################
    self.email = LabelFrame(self.grp, text = "None") #fill the right side of the subframe with an email reader
    self.email.pack(side=RIGHT)
    self.yscrollbar = Scrollbar(self.email) #put a scrollbar on the right
    self.yscrollbar.pack(side=RIGHT, fill=Y)

    self.text = Text(self.email, width=60, height=40,yscrollcommand=self.yscrollbar.set)
    self.text.insert(INSERT, "Hello......................................................................................................................")
    self.text.insert(END, "==================================================================================================================Bye Bye.....")
    self.text.config(state=DISABLED)
    self.text.pack()
    self.yscrollbar.config(command=self.text.yview)

    self.text.config(state=NORMAL)
    self.text.insert(END, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++whoBye Bye.....")
    self.text.config(state=DISABLED)
    self.email.config(text="MSP4_100_3")

######################## Control Subframes #################################
    self.ctls = Frame(self.top) #put a group subframe for stats in at the bottom of the window
    self.ctls.pack(side=TOP,fill=X)

    self.L1 = Label(self.ctls, text = "Hypothesis")
    self.L1.pack( side = LEFT)
    self.E1 = Entry(self.ctls, bd = 5)
    self.E1.pack(side = LEFT)

    #self.B = Button(self.ctls, text = "Hello", command = helloCallBack)
    self.B = Button(self.ctls, text = "Hello")
    self.B.pack(side = LEFT)

    #self.C = Button(self.ctls, text = "Bye", command = byeCallBack)
    self.C = Button(self.ctls, text = "Bye")
    self.C.pack(side = LEFT)

  #pointers to controller parts of callback operations are set her
  def setCtlBacks(self,helloBack, byeBack):
    self.B.config(command = helloBack)
    self.C.config(command = byeBack)
    #self.B = Button(self.top, text = "Hello", command = callback)
    #self.B.place(x = 50,y = 50)

  #view part of all callback operations go here
  def helloCallBack(self,title,words):
    self.msg = messagebox.showinfo(title,words)
  def byeCallBack(self,title,words):
    self.msg = messagebox.showinfo(title,words)
##all other stuff
#  def buttonChg(self,msg):
    self.B.config(text = msg)

  def run(self):
    self.top.mainloop()

