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
  def nextCback(self,fwd,mode,aiHypo): #move forward in emails
    if mode == "Read": #get next in email list
      (mailId,email,aiHypo,huHypo) = self.m.getReadMail(fwd) #forward read next email
    elif mode == "Search": #search for next that matches aiHypo
      (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(fwd,aiHypo) #forward search next AI email that matches hypo
    else:  #Train mode - train current email and fetch random untrained emails
      if fwd == True:
        mailId,email,aiHypo,huHypo = self.m.getNextTrain() #get next email to train
      else:
        mailId,email,aiHypo,huHypo = self.m.getPrevTrain() #get previous email to train
    return(mailId,email,aiHypo,huHypo) #view part of callback is here

  #def prevCback(self): #move backward in emails
  #  if mode == "Read": #get next in email list
  #    (mailId,email,aiHypo,huHypo) = self.m.getReadMail(True) #forward read next email
  #  elif mode == "Search": #search for next that matches aiHypo
  #    (mailId,email,aiHypo,huHypo) = self.m.getSearchMail(True,aiHypo) #forward search next AI email that matches hypo
  #  else:  #Train mode - train current email and fetch random untrained emails
  #    #mailId,email,aiHypo,huHypo = self.m.getNextTrain() #get next email to train
  #    mailId,email,aiHypo,huHypo = self.m.getPrevTrain() #get next email to train
  #  return(mailId,email,aiHypo,huHypo) #view part of callback is here

  #def chgTrain(self,huHypo,conf):
  def chgTrain(self,huHypo):
    trainCt,trainTrue = self.m.chgCurTrain(huHypo) #train current email
    #trainSz = int(self.trainSz(conf))
    #return(trainCt,trainTrue,trainSz)
    trueFract = '{:6.3f}'.format(trainTrue/trainCt*100)
    #return(trainCt,trainTrue)
    return(trainCt,trueFract)

  def gotoCback(self,gotoId): #dummy is the return character that we don't need
    return(self.m.getGotoMail(gotoId))

  def trainSz(self,conf):
    if self.m.trainCt == 0:
      tmp = 0.50
    else:
      tmp = self.m.trainTrue/self.m.trainCt
    return stats.samSz(int(conf)/100.0,tmp,self.m.mailCt)

  def trainConf(self,trainGoal,errMargin):
    aiConf = '{:6.2f}'.format(stats.samConf(int(trainGoal),float(errMargin),0.5,self.m.mailCt)*100)
    return aiConf

  #def errMargin(self,trainGoal,errMargin):
  #  conf = '{:6.2f}'.format(stats.samConf(int(trainGoal),float(errMargin),0.5,self.m.mailCt)*100)
  #  return conf

  def runAICback(self,errMargin,aiAlg):
    aiTrue,falsePos,falseNeg,aiOK = self.m.runAI(errMargin,aiAlg)
    trueFract = '{:6.3f}'.format(aiTrue/self.m.mailCt*100)
    #return(aiTrue,falsePos,falseNeg,aiOK)
    return(trueFract,falsePos,falseNeg,aiOK)

  def run(self,c):
    self.v.setVbacks(c)

    self.v.trainedLbl.setVal(self.m.trainCt) #set existing stats
    if self.m.trainCt != 0:
      trueFract = '{:6.3f}'.format(self.m.trainTrue/self.m.trainCt*100)
      self.v.trueLbl.setVal(trueFract)
    mailCt = self.m.mailCt
    self.v.mailCt.setVal(mailCt)
    trainGoal = int(mailCt*0.75)
    self.v.trainGoal.setVal(trainGoal)
    errMargin = 0.05
    self.v.errMargin.setVal(errMargin)
    aiConf = '{:6.2f}'.format(stats.samConf(trainGoal,errMargin,0.5,mailCt)*100)
    self.v.aiConf.setVal(aiConf)

    #conf = 75
    #self.v.conf.setVal(conf)
    #sz = self.trainSz(conf)
    #self.v.trainNeedLbl.setVal(int(sz))

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
    outfile = tmp
  else:
    aiSz = tmp[1:]
  try:
    tmp = sys.argv[3]
    if tmp[0] != '-':
      outfile = tmp
    else:
      aiSz = tmp[1:]
  except:
    pass
except:
  pass

v = view.view()
m = model.model(sys.argv[1],aiSz) #infile json
c = ctl(v,m)
c.run(c)
if outfile != None: #save the results 
  m.fileSv(outfile)

