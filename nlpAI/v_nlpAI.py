#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
from tkinter import *

from tkinter import messagebox

class lblVal():
  def __init__(self,root,label):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=TOP)
    #self.entry = Label(self.lblFr, text = val, width=10)
    self.val = Label(self.lblFr,  width=10)
    self.val.pack(side = TOP)

  def setVal(self,val):
    self.val.config(text = val)


class lblEntry():
  def __init__(self,root,label):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=TOP)
    self.entry = Entry(self.lblFr, width=10, bd=5)
    self.entry.pack(side = TOP)

  def getVal(self):
    return self.entry.get()

  def setVal(self,val):
    self.entry.insert(END,val)

class view():
  def __init__(self): #setup everything without controller callbacks
    #layout the frames in the top window
    self.top = Tk()
    self.grp = Frame(self.top) #put a group subframe for stats and email at the top of window
    self.grp.pack(side=TOP)

######################## Stats Subframe #################################
    self.stats = Frame(self.grp) #fill the left side of the grp subframe with a statistics frame
    self.stats.pack(side=LEFT,fill=Y)

    self.statsPad = Frame(self.stats,height=9)
    self.statsPad.pack(side = TOP)
    self.runAI = Button(self.stats, text = "runAI",width=10,height=2,bg='green')
    self.runAI.pack(side = TOP)
    self.conf = lblEntry(self.stats, 'confidence %')
    self.conf.setVal(75)
    self.trainResult = lblVal(self.stats, 'train result')
    self.trainNeedLbl = lblVal(self.stats, 'train needed')
    self.trainedLbl = lblVal(self.stats, 'trained')
    self.trueLbl = lblVal(self.stats, 'trained true')
    self.trueClass = lblVal(self.stats, 'AI true')
    self.falsePos = lblVal(self.stats, 'bad AI true')
    self.falseNeg = lblVal(self.stats, 'bad AI false')
    self.mailCt = lblEntry(self.stats, 'mail count')


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

    self.ctlsPad = Frame(self.ctls,width=5)
    self.ctlsPad.pack(side = TOP)
    self.ctlsPad.pack(side = RIGHT)
    self.prev = Button(self.ctls, text = "Prev")
    self.prev.pack(side = RIGHT)

    self.next = Button(self.ctls, text = "Next")
    self.next.pack(side = RIGHT)

    self.hypo = Button(self.ctls, width = 5)
    self.hypo.pack(side = RIGHT)

    self.hypoDsc = Entry(self.ctls, bd = 5)
    self.hypoDsc.pack(side = RIGHT)
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
  def setVbacks(self,hypoCback, nextCback,prevCback,modeCback,gotoCback,runAICback,confCback,mailCtCback):
    self.hypo.config(command = hypoCback)
    self.next.config(command = nextCback)
    self.prev.config(command = prevCback)
    self.mode.config(command = modeCback)
    self.goto.bind('<Return>', gotoCback)
    self.runAI.config(command = runAICback)
    self.conf.entry.bind('<Return>', confCback)
    self.mailCt.entry.bind('<Return>', mailCtCback)

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

