#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

#usage> python c_nlpAI.py srcFileNm.json, dstFileNm.json > dbg.txt
#srcFileNm = file containing all the emails to train and test
#dstFileNm = write the results of training and testing if sys.arv[2] exists. Overwrites srcFileNm if same.
import sys
import statsLib as stats
import v_nlpAI as view
import m_nlpAI as model

class ctl():
  def __init__(self,view,model):
    self.v = view
    self.m = model

  #create all the controller methods that the view object uses as callbacks
  def nextCback(self): #move forward in emails
    if self.v.mode['text'] == "Read": #get next in email list
      (mailId,email,aiHypo,huHypo) = self.m.getReadMail(True) #forward read next email
      self.v.aiHypo.setVal(aiHypo)
      self.v.huHypo.setVal(huHypo)
    elif self.v.mode['text'] == "Search": #search for next that matches aiHypo
      (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(True,self.v.aiHypo.getVal(),self.v.huHypo.getVal()) #forward search next AI email that matches hypo
      self.v.huHypo.setVal(huHypo)
    else:  #Train mode - train current email and fetch random untrained emails
      trainCt,trainTrue = self.m.chgCurTrain(self.v.huHypo.getVal()) #train current email
      self.v.trainedLbl.setVal(trainCt) #set training stats
      self.v.trueLbl.setVal(trainTrue)
      mailId,email,huHypo = self.m.getNextTrain() #get next email to train
      self.v.huHypo.setVal(huHypo)
    self.v.nextVback(mailId,email) #view part of callback is here

  def prevCback(self): #move backward in emails
    if self.v.mode['text'] == "Read":
      (mailId,email,aiHypo,huHypo) = self.m.getReadMail(False) #backward read next email
      self.v.aiHypo.setVal(aiHypo)
      self.v.huHypo.setVal(huHypo)
    elif self.v.mode['text'] == "Search":
      (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(False,self.v.aiHypo.getVal(),self.v.huHypo.getVal()) #forward search next AI email that matches hypo
      self.v.huHypo.setVal(huHypo)
    else: #Train mode
      mailId,email,huHypo = self.m.getPrevTrain() #get last trained email
    self.v.huHypo.setVal(huHypo)
    self.v.nextVback(mailId,email) #view part of callback is here
    return

  def gotoCback(self,dummy): #dummy is the return character that we don't need
    gotoId = self.v.getGotoId()  #get the mailID from the entry box
    mailId,email = self.m.getGotoMail(gotoId)
    self.v.gotoVback(mailId,email) #view part of callback is here
    return


  def confCback(self,dummy): #dummy is the return character that we don't need
    conf = self.v.conf.getVal()  #get the confidence value
    sz = stats.samSz(int(conf)/100.0,0.50,self.m.mailCt)
    self.v.trainNeedLbl.setVal(int(sz))
    return


  def mailCtCback(self,dummy): #dummy is the return character that we don't need
    conf = self.v.conf.getVal()  #get the confidence value
    self.m.mailCt = int(self.v.mailCt.getVal())  #get the size of the mail sample to use
    sz = stats.samSz(int(conf)/100.0,0.50,self.m.mailCt) #and recalculate the needed training size
    self.v.trainNeedLbl.setVal(int(sz))
    return

  def runAICback(self):
    self.m.runAI()
    self.v.trueClass.setVal(self.m.aiTrue)
    self.v.falsePos.setVal(self.m.falsePos)
    self.v.falseNeg.setVal(self.m.falseNeg)
    return

  def run(self):
    self.v.setVbacks(self.nextCback,self.prevCback,self.gotoCback,self.runAICback,self.confCback,self.mailCtCback) #give view pointers to controller callback methods

    self.v.trainedLbl.setVal(self.m.trainCt) #set existing stats
    self.v.trueLbl.setVal(self.m.trainTrue)
    self.v.mailCt.setVal(self.m.mailCt)

    (mailId,email,aiHypo,huHypo) = self.m.getReadMail(True) #point to first email to read
    self.v.aiHypo.setVal(aiHypo)
    self.v.huHypo.setVal(huHypo)
    self.v.nextVback(mailId,email) #view part of callback is here
    self.v.run() #run the tkinter loop

#create the view object first because it will be needed in callbacks
v = view.view()
m = model.model(sys.argv[1])
c = ctl(v,m)
try:
  dstfileNm = sys.argv[2]
except:
  dstfileNm = None
c.run()
if dstfileNm != None: #save the results 
  m.fileSv(dstfileNm)

