#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
import sys
import statsLib as stats
import v_nlpAI as view
import m_nlpAI as model

class ctl():
  def __init__(self,view,model):
    self.v = view
    self.m = model
    self.hypo = "True"
    self.mode = "Train"

  #create all the controller methods that the view object uses as callbacks
  def hypoCback(self):
  #put controller part of callback response here.......
    if self.hypo == "True":
      self.hypo = "False"
    else:
      self.hypo = "True"
    self.v.hypoVback(self.hypo) #view part of callback is here

  def nextCback(self):
    if self.mode == "Read":
      (mailId,email) = self.m.getReadMail(True)
    else:
      mailId,email = self.m.getNextTrain(self.hypo)
    self.v.trainedLbl.setVal(self.m.trainCt)
    self.v.trueLbl.setVal(self.m.trainTrue)
    self.v.nextVback(mailId,email) #view part of callback is here

  def prevCback(self):
    if self.mode == "Read":
      (mailId,email) = self.m.getReadMail(False)
    else:
      mailId,email,self.hypo = self.m.getPrevTrain()
    self.v.hypoVback(self.hypo)
    self.v.nextVback(mailId,email) #view part of callback is here
    return

  def modeCback(self):
  #put controller part of callback response here.......
    if self.mode == "Train":
      self.mode = "Search"
    elif self.mode == "Search":
      self.mode = "Read"
    else:
      self.mode = "Train"
    self.v.modeVback(self.mode) #view part of callback is here

  def gotoCback(self,dummy): #dummy is the return character that we don't need
    gotoId = self.v.getGotoId()  #get the mailID from the entry box
    mailId,email = self.m.getGotoMail(gotoId)
    self.v.gotoVback(mailId,email) #view part of callback is here
    return


  def confCback(self,dummy): #dummy is the return character that we don't need
    conf = self.v.conf.getVal()  #get the confidence value
    sz = stats.samSz(int(conf)/100.0,0.50,self.m.mailCt)
    self.v.trainNeedLbl.setVal(int(sz))
    #print('dbg0',conf)
    return

  def runAICback(self):
    return

  def run(self):
    self.v.hypoVback(self.hypo)
    self.v.modeVback(self.mode)
    self.v.setVbacks(self.hypoCback,self.nextCback,self.prevCback,self.modeCback,self.gotoCback,self.runAICback,self.confCback) #give view pointers to controller callback methods

    #self.v.trainNeedLbl.setVal('76')
    self.v.trainedLbl.setVal(self.m.trainCt)
    self.v.trueLbl.setVal(self.m.trainTrue)
    self.v.mailCt.setVal(self.m.mailCt)
    #self.v.trueClass.setVal('150')
    #self.v.falsePos.setVal('15')
    #self.v.falseNeg.setVal('15')
    self.v.run() #run the tkinter loop

#create the view object first because it will be needed in callbacks
v = view.view()
m = model.model(sys.argv[1])
c = ctl(v,m)
c.run()
