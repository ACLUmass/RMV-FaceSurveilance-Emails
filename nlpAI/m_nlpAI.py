#!/usr/bin/python3
import json
import random
import nlplibAI as ai

#email states
#AI       train       comment
#======================================================
#none     n/a         AI has not been run
#false    none        untrained negative
#true     none        untrained positive
#false    false       true negative
#true     true        true positive
#false    true        false negative - low sensitivity
#true     false       false positive - low specificity

class model():
  def __init__(self,fileNm,aiSz): #setup everything without controller callbacks
    #build a database of all the emails with images
    inf = open(fileNm, 'r')
    r = inf.read()  #read in all the bytes into one string
    self.mails = json.loads(r)
    self.idx = None 
    if aiSz == None:
      self.mailCt = len(self.mails)
    else:
      self.mailCt = int(aiSz)
    self.trainCt = 0
    self.trainTrue = 0
    self.aiTrue = 0
    self.falsePos = None
    self.falseNeg = None
    self.trains = [] #in train mode mailIdx moves forward randomly and backward by popping off this list
    for i in range(self.mailCt):
      if not 'ai' in self.mails[i]:
        self.mails[i]['ai'] = 'None'
      if 'train' in self.mails[i]:
        self.trainCt += 1
        if self.mails[i]['train'] == 'True':
          self.trainTrue += 1
      else:
        self.mails[i]['train'] = 'None'

  def fileSv(self,fileNm): #save the results
    with open(fileNm, 'w') as f:
      json.dump(self.mails, f)


  def formText(self,mail):
    text = 'From: ' + mail['from'] #format email for display
    text = text + '\n' + 'Date: '
    if mail['date'] != None:
      text = text + mail['date']
    text = text + '\n' + 'To: '
    if mail['to'] != None:
      text = text + mail['to']
    text = text + '\n' + 'cc: '
    if mail['cc'] != None:
      text = text + mail['cc']
    text = text + '\n' + 'attach: '
    if mail['attach'] != None:
      text = text + mail['attach']
    text = text + '\n' + 'subject: '
    if mail['subject'] != None:
      text = text + mail['subject']
    if mail['body'] != None:
      text = text + '\n' + mail['body']

    return(mail['mailId'],text)

  #change current training of current email its training stats
  def chgCurTrain(self,hypo):
    mail = self.mails[self.idx]
    if mail['train'] == 'None': #has not been trained yet
      self.trainCt += 1
      if hypo == 'True':
        self.trainTrue += 1
    else:  #previously trained
      if hypo != mail['train']: #changing training
        if hypo == 'True': #false to true
          self.trainTrue += 1
        else: #true to false
          self.trainTrue -= 1
    self.mails[self.idx]['train'] = hypo
    return(self.trainCt, self.trainTrue)
          

  #add training to current email and fetch a new random one to train
  def getNextTrain(self):
    if self.trainCt == self.mailCt: #nothing left to train
      return('none','all trained','None')
    self.trains.append(self.idx) #put current idx on list for going in reverse
    while True: #find a mail that has not been trained already
      self.idx = random.randint(0,self.mailCt - 1) 
      mail = self.mails[self.idx]
      if mail['train'] == 'None':
        break

    mailId,email =  self.formText(mail)
    return(mailId,email,mail['ai'],'None')

  #update training to current email and fetch previously trained email plus its training
  def getPrevTrain(self):
    if len(self.trains) == 0: #walked all the way back
      self.idx = None
      return('none','all the way back','')
    self.idx = self.trains.pop()

    mail = self.mails[self.idx]
    mailId,email =  self.formText(mail)
    return(mailId,email,mail['train'])

  #get next or previous email linearly plus its current AI state
  def getReadMail(self,fwd):
    if fwd == True: #move the index forward.
      if self.idx == None:
        self.idx = 0
      elif self.idx < self.mailCt:
        self.idx += 1
    else: #move index backward
      if self.idx == None:
        self.idx = self.mailCt - 1
      elif self.idx > -1:
        self.idx -= 1

    if self.idx == self.mailCt or self.idx == -1: #signal that index is out of bounds
      return('none','out of bounds','','')
    else: #get the email
      mail = self.mails[self.idx]
      tmp = self.formText(mail)
      if 'ai' in mail.keys():
        aiHypo = mail['ai']
      else:
        aiHypo = 'None'
      if 'train' in mail.keys():
        huHypo = mail['train']
      else:
        huHypo = 'None'
      return(tmp[0],tmp[1],aiHypo,huHypo)


  #get next or previous email that matches AI hypo
  def getSearchMail(self,fwd,aiHypoIn):
    while True:
      mailId,email,aiHypo,huHypo = self.getReadMail(fwd)
      if mailId == 'none' or aiHypoIn == aiHypo:
        break
    return(mailId,email,aiHypo,huHypo)


  #goto a mailId
  def getGotoMail(self,gotoId):
    for self.idx in range(0,self.mailCt): #search from the beginning
      if self.mails[self.idx]['mailId'] == gotoId:
        break
    else: #didn't find a match
      return('none','not found')

    mail = self.mails[self.idx]
    mailId,email =  self.formText(mail) #found it!
    return(mailId,email,mail['ai'],mail['train'])

  def runAI(self):
    rawMail = []  #byte form of each email
    allBows = []  #byte representaton of all emails

    for i in range(self.mailCt): #create email list
      mail = self.mails[i]
      mailId,email =  self.formText(mail) #convert to byte form
      email = email.replace(u'\xa0', u' ') #replace nonbreaking space with a real one
      tmp = email.encode('UTF-8')
      rawMail.append(tmp)
    allBows = ai.mkBow(rawMail)  #turn raw mail into bag of words


    allSets = ai.mkSet(allBows)
    trainSets = [] #byte representaton of training set
    trainHypos = []  #training hypos for training set. 1=true, 0=false
    trainPtrs = []   #pointer for training set into test set
    for i in range(self.mailCt): #create training sets
      mail = self.mails[i]
      if 'train' in mail.keys(): #copy the training set
        trainSets.append(allSets[i])
        trainPtrs.append(i)
        if mail['train'] == 'True':
          trainHypos.append(1)
        else:
          trainHypos.append(0)

    allHypos = ai.rfa(trainSets,allSets,trainHypos)
    self.aiTrue = 0
    for i in range(self.mailCt): #create training sets
      if allHypos[i] == 1:
        self.mails[i]['ai'] = 'True'
        self.aiTrue += 1
      else:
        self.mails[i]['ai'] = 'False'

    self.falsePos = 0
    self.falseNeg = 0
    for i in range(self.trainCt):
      ptr = trainPtrs[i] 
      aiHypo = self.mails[ptr]['ai']
      huHypo = self.mails[ptr]['train']
      if aiHypo != 'None' and huHypo != 'None': 
        if aiHypo != huHypo: #by definition the human is always right 
          if aiHypo == 'True':
            self.falsePos += 1
          else:
            self.falseNeg += 1

    return(self.aiTrue,self.falsePos,self.falseNeg)      
