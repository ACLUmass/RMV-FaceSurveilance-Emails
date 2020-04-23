#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
from tkinter import *

from tkinter import messagebox

class lblVal():
  def __init__(self,root,label,val):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=TOP)
    self.entry = Label(self.lblFr, text = val, width=10)
    self.entry.pack(side = TOP)


class lblEntry():
  def __init__(self,root,label,entry):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=TOP)
    self.entry = Entry(self.lblFr, text = entry, width=10, bd=5)
    self.entry.pack(side = TOP)


class view():
  def __init__(self): #setup everything without controller callbacks
    #layout the frames in the top window
    self.top = Tk()
    self.grp = Frame(self.top) #put a group subframe for stats and email at the top of window
    self.grp.pack(side=TOP)

######################## Stats Subframe #################################
    self.stats = Frame(self.grp) #fill the left side of the grp subframe with a statistics frame
    self.stats.pack(side=LEFT,fill=Y)

    self.runAI = Button(self.stats, text = "runAI")
    self.runAI.pack(side = TOP)

    self.trainOk = Button(self.stats, text = "good")
    self.trainOk.pack(side = TOP)

    #self.confidenceLbl = lblEntry(self.stats, 'confidence %', '95')
    #self.trainOk = StringVar()
    #self.trainOkLbl = Label(self.stats, textvariable = self.trainOk)
    #self.trainOkLbl.pack(side=TOP)

    self.confidenceLbl = lblEntry(self.stats, 'confidence %', '95')

    self.trainNeedLbl = lblVal(self.stats, 'train needed', '76')

    self.trainedLbl = lblVal(self.stats, 'trained', '33')

    self.trueLbl = lblVal(self.stats, 'True', '15')

    self.classified = lblVal(self.stats, 'classified', '1500')

    self.trueClass = lblVal(self.stats, 'True Class', '150')

    self.falsePos = lblVal(self.stats, 'False Pos', '15')

    self.falseNeg = lblVal(self.stats, 'False Neg', '15')


################# Email Reader Subframe ################################
    self.email = LabelFrame(self.grp, text = 'none') #fill the right side of the subframe with an email reader
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

    self.prev = Button(self.ctls, text = "Prev")
    self.prev.pack(side = RIGHT)

    self.next = Button(self.ctls, text = "Next")
    self.next.pack(side = RIGHT)

    self.hypo = Button(self.ctls, width = 5)
    self.hypo.pack(side = RIGHT)

    self.E1 = Entry(self.ctls, bd = 5)
    self.E1.pack(side = RIGHT)
    self.L1 = Label(self.ctls, text = "Class")
    self.L1.pack( side = RIGHT)

    self.mode = Button(self.ctls, width=6)
    self.mode.pack(side = RIGHT)

    self.L2 = Label(self.ctls, text = "Goto")
    self.L2.pack( side = LEFT)
    self.goto = Entry(self.ctls, bd = 5, width=15)
    self.goto.pack(side = LEFT)

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
    self.hypo.config(command = hypoCback)
    self.next.config(command = nextCback)
    self.prev.config(command = prevCback)
    self.mode.config(command = modeCback)
    self.goto.bind('<Return>', gotoCback)
    self.runAI.config(command = runAICback)

  def getGotoId(self): #get the contents of goto Entry box
    return self.goto.get()

  #view part of all callback operations go here
  def hypoVback(self,msg):
    self.hypo.config(text = msg)

  def nextVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def prevVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def modeVback(self,msg):
    self.mode.config(text = msg)

  def gotoVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def runAIVback(self,msg):
    self.runAI.config(text = msg)

