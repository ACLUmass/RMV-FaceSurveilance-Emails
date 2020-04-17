#!/usr/bin/python3
import json
import random

class model():
  def __init__(self,fileNm): #setup everything without controller callbacks
    #build a database of all the emails with images
    inf = open(fileNm, 'r')
    r = inf.read()  #read in all the bytes into one string
    self.mails = json.loads(r)
    self.mailCt = len(self.mails)
    self.trainCt = 0
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
    text = text + '\n' + mail['body']

    return(mail['mailId'],text)

  #
  def getTrainMail(self,fwd):
    if fwd == True: #randomly pick untrained email
      if self.trainCt == self.mailCt: #nothing left to train
        return('none','all trained')
      while True: #find a mail that has not been trained already
        idx = random.randint(0,self.mailCt - 1) 
        if not 'train' in  self.mails[idx].keys():
          break
      if self.idx != None:
        self.trains.append(self.idx) #put idx on list for going in reverse
      self.idx = idx
    else:
      if len(self.trains) == 0: #walked all the way back
        self.idx = None
        return('none','all the way back')
      self.idx = self.trains.pop()

    mail = self.mails[self.idx]
    return(self.formText(mail))

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

