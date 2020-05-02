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
  def nextCback(self,mode,aiHypo): #move forward in emails
    if mode == "Read": #get next in email list
      (mailId,email,aiHypo,huHypo) = self.m.getReadMail(True) #forward read next email
      #self.v.aiHypo.setVal(aiHypo)
      #self.v.huHypo.setVal(huHypo)
    elif mode == "Search": #search for next that matches aiHypo
      (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(True,aiHypo) #forward search next AI email that matches hypo
      #self.v.huHypo.setVal(huHypo)
    else:  #Train mode - train current email and fetch random untrained emails
      mailId,email,aiHypo,huHypo = self.m.getNextTrain() #get next email to train
      #self.v.huHypo.setVal(huHypo)
    return(mailId,email,aiHypo,huHypo) #view part of callback is here

  def prevCback(self): #move backward in emails
    if self.v.mode['text'] == "Read":
      (mailId,email,aiHypo,huHypo) = self.m.getReadMail(False) #backward read next email
      self.v.aiHypo.setVal(aiHypo)
      self.v.huHypo.setVal(huHypo)
    elif self.v.mode['text'] == "Search":
      (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(False,self.v.aiHypo.getVal(),self.v.huHypo.getVal()) #forward search next AI email that matches hypo
      self.v.huHypo.setVal(huHypo)
    else: #Train mode
      self.chgTrain()
      mailId,email,huHypo = self.m.getPrevTrain() #get previous email trained
      self.v.huHypo.setVal(huHypo)
    self.v.nextVback(mailId,email) #view part of callback is here
    return

  def chgTrain(self,huHypo):
    trainCt,trainTrue = self.m.chgCurTrain(huHypo) #train current email
    self.v.trainedLbl.setVal(trainCt) #set training stats
    self.v.trueLbl.setVal(trainTrue)
    self.trainSz()
    return

  def modeCback(self):
    mode = self.v.mode['text']  #get the current mode
    if mode == 'Train': #leaving training so save latest training
      self.chgTrain()
    self.v.modeVback() #go to new mode
    return


  def gotoCback(self,gotoId): #dummy is the return character that we don't need
    return(self.m.getGotoMail(gotoId))

  def trainSz(self,conf):
    #conf = self.v.conf.getVal()  #get the confidence value
    if self.m.trainCt == 0:
      tmp = 0.50
    else:
      tmp = self.m.trainTrue/self.m.trainCt
    return stats.samSz(int(conf)/100.0,tmp,self.m.mailCt)

  def confCback(self,dummy): #dummy is the return character that we don't need
    self.trainSz()
    return


  def mailCtCback(self,dummy): #dummy is the return character that we don't need
    self.m.mailCt = int(self.v.mailCt.getVal())  #get the size of the mail sample to use
    self.trainSz()
    return

  def runAICback(self):
    aiTrue,falsePos,falseNeg = self.m.runAI()
    return(aiTrue,falsePos,falseNeg)

  def dbg(self,tmp):
    print('dbg0 ',tmp)

  def run(self,c):
    self.v.setVbacks(c,self.modeCback,self.nextCback,self.prevCback,self.gotoCback,self.runAICback,self.confCback,self.mailCtCback) #give view pointers to controller callback methods

    self.v.trainedLbl.setVal(self.m.trainCt) #set existing stats
    self.v.trueLbl.setVal(self.m.trainTrue)
    self.v.mailCt.setVal(self.m.mailCt)

    conf = 75
    self.v.conf.setVal(conf)
    sz = self.trainSz(conf)
    self.v.trainNeedLbl.setVal(int(sz))


    (mailId,email,aiHypo,huHypo) = self.m.getReadMail(True) #point to first email to read
    self.v.aiHypo.setVal(aiHypo)
    self.v.huHypo.setVal(huHypo)
    self.v.ldEmail(mailId,email) #view part of callback is here
    self.v.run() #run the tkinter loop

#create the view object first because it will be needed in callbacks
outfile = None
aiSz = None
try:
  tmp = sys.argv[2]
  if tmp[0] != '-':
    dstFileNm = tmp
  else:
    aiSz = tmp[1:]
  try:
    tmp = sys.argv[3]
    if tmp != '-':
      dstFileNm = tmp
    else:
      aiSz = tmp[1:]
  except:
    pass
except:
  pass

v = view.view()
m = model.model(sys.argv[1],aiSz) #infile json
c = ctl(v,m)
#try:
#  dstfileNm = sys.argv[2]
#except:
#  dstfileNm = None
c.run(c)
if dstfileNm != None: #save the results 
  m.fileSv(dstfileNm)

