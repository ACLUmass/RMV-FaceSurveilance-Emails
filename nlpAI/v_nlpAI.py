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

    #self.E = Button(self.ctls, text = "Bye", command = byeCallBack)
    self.F = Button(self.stats, text = "runAI")
    self.F.pack(side = TOP)

    self.trainCtLbl = Label(self.stats, text = 'trainCt')
    self.trainCtLbl.pack(side=TOP)

    self.trainCt = StringVar()
    self.trainCtDat = Label(self.stats, textvariable = self.trainCt, relief = RAISED )

    self.trainCt.set("430")
    self.trainCtDat.pack(side=TOP)



################# Email Reader Subframe ################################
    self.email = LabelFrame(self.grp) #fill the right side of the subframe with an email reader
    self.email.pack(side=RIGHT)
    self.yscrollbar = Scrollbar(self.email) #put a scrollbar on the right
    self.yscrollbar.pack(side=RIGHT, fill=Y)

    self.text = Text(self.email, width=80, height=50,yscrollcommand=self.yscrollbar.set)
    self.text.config(state=DISABLED)
    self.text.pack()
    self.yscrollbar.config(command=self.text.yview)

    self.text.config(state=DISABLED)

######################## Control Subframes #################################
    self.ctls = Frame(self.top) #put a group subframe for stats in at the bottom of the window
    self.ctls.pack(side=TOP,fill=X)

    self.D = Button(self.ctls, text = "Prev")
    self.D.pack(side = RIGHT)

    self.C = Button(self.ctls, text = "Next")
    self.C.pack(side = RIGHT)

    self.B = Button(self.ctls)
    self.B.pack(side = RIGHT)

    self.E1 = Entry(self.ctls, bd = 5)
    self.E1.pack(side = RIGHT)
    self.L1 = Label(self.ctls, text = "Class")
    self.L1.pack( side = RIGHT)

    self.E = Button(self.ctls, text = "Train")
    self.E.pack(side = RIGHT)

    self.L2 = Label(self.ctls, text = "Goto")
    self.L2.pack( side = LEFT)
    self.E2 = Entry(self.ctls, bd = 5, width=15)
    self.E2.pack(side = LEFT)

##all other stuff
  def run(self):
    self.top.mainloop()

  def ldEmail(self,mailId,email):
    self.email.config(text=mailId)
    self.text.config(state=NORMAL)
    self.text.delete(1.0,END)
    self.text.insert(INSERT, email)
    self.text.config(state=DISABLED)

  #pointers to controller parts of callback operations are set her
  def setVbacks(self,hypoCback, nextCback,prevCback,modeCback,gotoCback,runAICback):
    self.B.config(command = hypoCback)
    self.C.config(command = nextCback)
    self.D.config(command = prevCback)
    self.E.config(command = modeCback)
    self.E2.bind('<Return>', gotoCback)
    self.F.config(command = runAICback)

  #view part of all callback operations go here
  def hypoVback(self,msg):
    self.B.config(text = msg)

  def nextVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def prevVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def modeVback(self,msg):
    self.E.config(text = msg)

  def gotoVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def runAIVback(self,msg):
    self.F.config(text = msg)

