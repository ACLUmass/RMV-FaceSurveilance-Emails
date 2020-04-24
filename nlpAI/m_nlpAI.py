#!/usr/bin/python3
import json
import random

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
  def __init__(self,fileNm): #setup everything without controller callbacks
    #build a database of all the emails with images
    inf = open(fileNm, 'r')
    r = inf.read()  #read in all the bytes into one string
    self.mails = json.loads(r)
    self.mailCt = len(self.mails)
    self.trainCt = 0
    self.trainTrue = 0
    self.idx = None
    self.trains = [] #in train mode mailIdx moves forward randomly and backward by popping off this list

  def formText(self,mail):
    text = 'From: ' + mail['from'] + '\n' + 'Date: ' + mail['date'] #format email for display
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
    text = text + '\n' + mail['body']

    return(mail['mailId'],text)

  #add training to current email and fetch a new random one to train
  def getNextTrain(self,hypo):
    if self.trainCt == self.mailCt: #nothing left to train
      return('none','all trained')
    while True: #find a mail that has not been trained already
      idx = random.randint(0,self.mailCt - 1) 
      if not 'train' in  self.mails[idx].keys():
        break
    if self.idx != None:
      self.mails[self.idx]['train'] = hypo
      self.trainCt += 1
      if hypo == "True":
        self.trainTrue += 1
      self.trains.append(self.idx) #put idx on list for going in reverse
    self.idx = idx

    mail = self.mails[self.idx]
    mailId,email =  self.formText(mail)
    return(mailId,email)

  #update training to current email and fetch previously trained email plus its training
  def getPrevTrain(self):
    if len(self.trains) == 0: #walked all the way back
      self.idx = None
      return('none','all the way back','None')
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
      return('none','out of bounds')
    else: #get the email
      mail = self.mails[self.idx]
      return(self.formText(mail))

  #goto a mailId
  def getGotoMail(self,gotoId):
    for self.idx in range(0,self.mailCt): #search from the beginning
      if self.mails[self.idx]['mailId'] == gotoId:
        break
    else: #didn't find a match
      return('none','not found')

    mail = self.mails[self.idx]
    mailId,email =  self.formText(mail) #found it!
    return(mailId,email)
