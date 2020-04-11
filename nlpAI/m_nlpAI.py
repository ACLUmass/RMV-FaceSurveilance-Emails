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
    self.idx = 0

  #
  def getMail(self):
    if self.trainCt == self.mailCt: #nothing left to train
      return None
    while True: #find a mail that has not been trained already
      self.idx = random.randint(0,self.mailCt - 1) 
      if not 'train' in  self.mails[self.idx].keys():
        mail = self.mails[self.idx]
        break
    
    text = 'From: ' + mail['from'] + '\n' + 'Date: ' + mail['date'] #format email for display
    if 'to' in mail.keys():
      text = text + '\n' + 'To: ' + mail['to']
    if 'cc' in mail.keys():
      text = text + '\n' + 'cc: ' + mail['cc']
    text = text + '\n' + mail['body']

    return(mail['mailId'],text)


