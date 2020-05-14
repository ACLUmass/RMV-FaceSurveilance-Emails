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
    self.lblFr = LabelFrame(root, text = label)
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
    return self.button['text']

  def setVal(self,val):
    self.button.config(text = val)
    if val == 'True':
      self.lblFr.config(bg='#7fff7f')
    elif val == 'False':
      self.lblFr.config(bg='#ff7f7f')
    else:
      self.lblFr.config(bg='#ffffff')
      

class aiAlgButton():
  def __init__(self,root,label,wd):
    self.lblFr = LabelFrame(root, text = label)
    self.lblFr.pack(side=RIGHT)
    self.button = Button(self.lblFr, width = wd)
    self.button.pack(side = RIGHT)
    self.lblFr.config(bg='#7f7fff')

  def getVal(self):
    return self.button['text']

  def setVal(self,val):
    self.button.config(text = val)
      

class view():
  def __init__(self): #setup everything without controller callbacks
    #layout the frames in the top window
    self.top = Tk()
    self.c = None
    self.top.title('Email AI Classifier')
    self.grp = Frame(self.top) #put a group subframe for stats and email at the top of window
    self.grp.pack(side=TOP)

######################## Stats Subframe #################################
    self.stats = Frame(self.grp) #fill the left side of the grp subframe with a statistics frame
    self.stats.pack(side=LEFT,fill=Y)

    self.statsPad = Frame(self.stats,height=9)
    self.statsPad.pack(side = TOP)
    self.runAI = Button(self.stats, text = "runAI",width=10,height=2)
    self.runAI.pack(side = TOP)
    self.aiAlg = aiAlgButton(self.stats, 'aiAlg', 10)
    self.aiAlg.lblFr.pack(side = TOP)
    self.aiOK = lblVal(self.stats, 'AI OK',10)
    self.trainGoal = lblEntry(self.stats, 'train goal',10)
    self.trainGoal.lblFr.pack(side=TOP)
    self.errMargin = lblEntry(self.stats, 'err margin %',10)
    self.errMargin.lblFr.pack(side=TOP)
    self.aiConf = lblVal(self.stats, 'AI confidence %',10)
    self.spacer = Label(self.stats, height=4, text = "")
    self.spacer.pack( side = TOP)
    #self.conf = lblEntry(self.stats, 'confidence %',10)
    #self.conf.lblFr.pack(side=TOP)
    #self.trainNeedLbl = lblVal(self.stats, 'train size',10)
    self.trainedLbl = lblVal(self.stats, 'trained size',10)
    self.trueLbl = lblVal(self.stats, 'trained true %',10)
    self.mailCt = lblVal(self.stats, 'AI Size',10)
    self.trueClass = lblVal(self.stats, 'AI true %',10)
    self.falsePos = lblVal(self.stats, 'bad AI true',10)
    self.falseNeg = lblVal(self.stats, 'bad AI false',10)


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
    self.ctlsPad.pack(side = RIGHT)

    self.mode = Button(self.ctls, text = 'Read', width=6, height=2)
    self.mode.pack(side = RIGHT)

    self.prev = Button(self.ctls, text = "Prev", height=2)
    self.prev.pack(side = RIGHT)

    self.next = Button(self.ctls, text = "Next", height=2)
    self.next.pack(side = RIGHT)

    self.huHypo = lblButton(self.ctls, 'human',6)
    self.huHypo.lblFr.pack(side=RIGHT)

    self.aiHypo = lblButton(self.ctls, 'ai',6)
    self.aiHypo.lblFr.pack(side=RIGHT)

    self.hypoDsc = Entry(self.ctls, bd = 5)
    self.hypoDsc.pack(side = RIGHT)
    self.L1 = Label(self.ctls, text = "Hypo")
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

  def aiAlgVback(self):
    tmp = self.aiAlg.getVal()
    if tmp == 'rfa':
      self.aiAlg.setVal('svm')
    elif tmp == 'svm':
      self.aiAlg.setVal('nvb')
    else:
      self.aiAlg.setVal('rfa')


  def huHypoVback(self):
    if self.mode['text'] == 'Train': #user change allowed only in train mode
      tmp = self.huHypo.getVal()
      if tmp == 'None':
        tmp = 'False'
      elif tmp == 'False':
        tmp = 'True'
      else:
        tmp = 'False'
      self.huHypo.setVal(tmp)
      #trainCt,trainTrue,trainSz = self.c.chgTrain(tmp,self.conf.getVal())
      trainCt,trainTrue = self.c.chgTrain(tmp)
      self.trainedLbl.setVal(trainCt) #set training stats
      #self.aiConf.setVal(aiConf) #set training stats
      self.trueLbl.setVal(trainTrue)
      #self.trainNeedLbl.setVal(trainSz)

  def aiHypoVback(self):
    if self.mode['text'] == 'Search': #user change allowed because search is on aiHypo
      tmp = self.aiHypo.getVal()
      if tmp == 'True':
        self.aiHypo.setVal('False')
      else:
        self.aiHypo.setVal('True')

  #def confVback(self,dummy): #dummy is the return character that we don't need
  #  sz = self.c.trainSz(self.conf.getVal())
  #  self.trainNeedLbl.setVal(int(sz))

  def trGoalVback(self,dummy): #dummy is the return character that we don't need
    conf = self.c.trainConf(self.trainGoal.getVal(),self.errMargin.getVal())
    #self.aiConf.setVal('{:6.2f}'.format(conf))
    self.aiConf.setVal(conf)

  def errMarginVback(self,dummy): #dummy is the return character that we don't need
    conf = self.c.errMargin(self.trainGoal.getVal(),self.errMargin.getVal())
    #self.aiConf.setVal('{:6.2f}'.format(conf))
    self.aiConf.setVal(conf)

  def getGoto(self,dummy): #get the contents of goto Entry box
    mailId,email,aiHypo,huHypo = self.c.gotoCback(self.goto.get())
    self.ldEmail(mailId,email)
    self.aiHypo.setVal(aiHypo)
    self.huHypo.setVal(huHypo)

  def nextVback(self):
    mailId,email,aiHypo,huHypo = self.c.nextCback(True,self.mode['text'],self.aiHypo.getVal())
    self.aiHypo.setVal(aiHypo)
    self.huHypo.setVal(huHypo)
    self.ldEmail(mailId,email)

  def prevVback(self):
    #if self.mode['text'] != 'Train':
    mailId,email,aiHypo,huHypo = self.c.nextCback(False,self.mode['text'],self.aiHypo.getVal())
    self.aiHypo.setVal(aiHypo)
    self.huHypo.setVal(huHypo)
    self.ldEmail(mailId,email)

  def runAIVback(self):
    aiTrue,falsePos,falseNeg,aiOK = self.c.runAICback(float(self.errMargin.getVal()),self.aiAlg.getVal())
    self.trueClass.setVal(aiTrue)
    self.falsePos.setVal(falsePos)
    self.falseNeg.setVal(falseNeg)
    if aiOK == True:
      self.aiOK.setVal('Pass')
      self.aiOK.lblFr.config(bg='#7fff7f')
    else:
      self.aiOK.setVal('Fail')
      self.aiOK.lblFr.config(bg='#ff7f7f')

    
 
  #pointers to controller parts of callback operations are set her
  def setVbacks(self,c):
    self.c = c
    self.huHypo.button.config(command = self.huHypoVback)
    self.aiHypo.button.config(command = self.aiHypoVback)
    self.aiAlg.button.config(command = self.aiAlgVback)
    self.mode.config(command = self.modeVback)
    self.goto.bind('<Return>', self.getGoto)
    #self.conf.entry.bind('<Return>', self.confVback)
    self.runAI.config(command = self.runAIVback)
    self.next.config(command = self.nextVback)
    self.prev.config(command = self.prevVback)
    self.trainGoal.entry.bind('<Return>', self.trGoalVback)
    self.errMargin.entry.bind('<Return>', self.trGoalVback)
    self.aiAlg.setVal('rfa')

