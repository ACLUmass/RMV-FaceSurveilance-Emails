#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
from tkinter import *

from tkinter import messagebox

class lblVal():
  def __init__(self,root,label,wd):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=TOP)
    self.val = Label(self.lblFr,  width=wd)
    self.val.pack(side = TOP)

  def setVal(self,val):
    self.val.config(text = val)


class lblEntry():
  def __init__(self,root,label,wd):
    #self.lblFr = LabelFrame(root, text = label, labelanchor = 'w')
    self.lblFr = LabelFrame(root, text = label)
    #self.lblFr.pack(side=TOP)
    self.entry = Entry(self.lblFr, width=wd, bd=5)
    self.entry.pack(side = TOP)

  def getVal(self):
    return self.entry.get()

  def setVal(self,val):
    self.entry.insert(END,val)


class lblButton():
  def __init__(self,root,label,wd):
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=RIGHT)
    self.button = Button(self.lblFr, width = wd)
    self.button.pack(side = RIGHT)

  def getVal(self):
    #return self.button.get()
    return self.button['text']

  def setVal(self,val):
    self.button.config(text = val)

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
    self.conf = lblEntry(self.stats, 'confidence %',10)
    self.conf.lblFr.pack(side=TOP)
    self.conf.setVal(75)
    self.trainResult = lblVal(self.stats, 'train result',10)
    self.trainNeedLbl = lblVal(self.stats, 'train needed',10)
    self.trainedLbl = lblVal(self.stats, 'trained',10)
    self.trueLbl = lblVal(self.stats, 'trained true',10)
    self.trueClass = lblVal(self.stats, 'AI true',10)
    self.falsePos = lblVal(self.stats, 'bad AI true',10)
    self.falseNeg = lblVal(self.stats, 'bad AI false',10)
    self.mailCt = lblEntry(self.stats, 'mail count',10)
    self.mailCt.lblFr.pack(side=TOP)


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
    #self.ctlsPad.pack(side = TOP)
    self.ctlsPad.pack(side = RIGHT)

    self.mode = Button(self.ctls, text = 'Read', width=6, height=2)
    self.mode.pack(side = RIGHT)

    self.prev = Button(self.ctls, text = "Prev", height=2)
    self.prev.pack(side = RIGHT)

    self.next = Button(self.ctls, text = "Next", height=2)
    self.next.pack(side = RIGHT)

    #self.hypo = Button(self.ctls, width = 5)
    self.huHypo = lblButton(self.ctls, 'human',6)
    self.huHypo.lblFr.pack(side=RIGHT)

    self.aiHypo = lblButton(self.ctls, 'ai',6)
    self.aiHypo.lblFr.pack(side=RIGHT)
    #self.hypo.pack(side = RIGHT)

    self.hypoDsc = Entry(self.ctls, bd = 5)
    self.hypoDsc.pack(side = RIGHT)
    self.L1 = Label(self.ctls, text = "Class")
    self.L1.pack( side = RIGHT)

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

  def modeVback(self):
    tmp = self.mode['text']
    if tmp == 'Read':
      self.mode.config(text = 'Search')
    elif tmp == 'Search':
      self.mode.config(text = 'Train')
    else:
      self.mode.config(text = 'Read')

  def huHypoVback(self):
    if self.mode['text'] == 'Train': #user change allowed only in train mode
      tmp = self.huHypo.getVal()
      if tmp == 'True':
        self.huHypo.setVal('False')
      else:
        self.huHypo.setVal('True')

  def aiHypoVback(self):
    if self.mode['text'] == 'Search': #user change allowed because search is on aiHypo
      tmp = self.aiHypo.getVal()
      if tmp == 'True':
        self.aiHypo.setVal('False')
      else:
        self.aiHypo.setVal('True')



  #pointers to controller parts of callback operations are set her
  def setVbacks(self,nextCback,prevCback,gotoCback,runAICback,confCback,mailCtCback):
    self.mode.config(command = self.modeVback)
    self.huHypo.button.config(command = self.huHypoVback)
    self.aiHypo.button.config(command = self.aiHypoVback)

    self.next.config(command = nextCback)
    self.prev.config(command = prevCback)
    self.goto.bind('<Return>', gotoCback)
    self.runAI.config(command = runAICback)
    self.conf.entry.bind('<Return>', confCback)
    self.mailCt.entry.bind('<Return>', mailCtCback)

  def getGotoId(self): #get the contents of goto Entry box
    return self.goto.get()

  def nextVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def prevVback(self,mailId,email):
    self.ldEmail(mailId,email)
  def gotoVback(self,mailId,email):
    self.ldEmail(mailId,email)

  def runAIVback(self,msg):
    self.runAI.config(text = msg)

