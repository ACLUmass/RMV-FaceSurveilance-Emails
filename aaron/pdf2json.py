import sys
import re
import json
import pdfplumber
from tabulate import tabulate


#works with output from  pdf2txt.py msp_p1.pdf > msp_p1.txt
fromCt = 0
pageCt = 0
dateCt = 0
toCt = 0
ccCt = 0
subjCt = 0
atchCt = 0
pages = []
alltxt = ''

#extract text from pdf
def pdf2txt(filename):
  doc = None
  with pdfplumber.open(filename) as pdf:
    i = 0
    while True:
     try:
       first_page = pdf.pages[i]
     except:
       break  #quit when we run out of pages
     page = first_page.extract_text(x_tolerance=1, y_tolerance=1)
     if doc != None: #no page break before first email
       doc += '\f'
     else:
       doc = ''
     if page: #some pages are blank
       doc += page
     i += 1

  doc += '\f' #need one at the end
  return doc

#make an email record from the single text string of that email
def mkMailRec(mailNo,mailId,txt):
  email = {}
  email['mailNo'] = mailNo #useful for debugger breakpoints
  email['mailId'] = mailId #useful for locating email in pdf
  lines = txt.splitlines() 
  #for key in ['from','to','date','sent','cc','subject']:
  for key in ['from','to','date','sent','cc']:
    for i in range(len(lines)):
      #chk = re.match('\s*' + key + ':',lines[i],re.IGNORECASE)
      chk = re.match('>*\s*' + key + ':',lines[i],re.IGNORECASE)
      if chk:
        line = lines.pop(i)
        keyEnd = chk.span()[1]
        if keyEnd < len(line):
          email[key] = line[keyEnd:] 
        else:  #there are a few cases where the data ends up on the next line
          if i < len(lines):  #we have a next line
            email[key] = lines.pop(i)
          else:
            email[key] = None
        break
    else:
      email[key] = None

  if email['date'] == None:
    email['date'] = email.pop('sent') #only one for these two will exist

  if len(lines) > 0:
    email['body'] = ''.join(lines) #what's left is the body
  else:
    email['body'] =  None
    
  return email

 
#sys.argv[1] is a json file (no json extention) of all the mail pdfs
#[['prefix','filename'],....]

#sys.argv[2] is the json file to create without the json extension

mailList = open(sys.argv[1] + '.json', 'r')
r = mailList.read()  #read in all the bytes into one string
pdfs = json.loads(r)

for pdf in pdfs: #go thru each pdf in the list
  srcId = pdf[0]   #which rmv pdf this text came from
  txt = pdf2txt(pdf[1] + '.pdf') #convert the pdf to text

  #these stats are for debugging quick checks
  pageCt = 0 #should equal last page number in pdf
  mailCt = 0 #should equal the number of emails in the pdf and the last mailNo

  #find the character location of each page break in the text string
  brklocs = []
  brks = re.finditer('\f',txt,re.IGNORECASE)
  for brk in brks:
    pageCt += 1
    brklocs.append(brk.span()[0])

  #find the character location of start of each email in the text string
  frlocs = []
  frs = re.finditer('From:',txt,re.IGNORECASE)
  for fr in frs:
    frlocs.append(fr.span()[0])

  #create a tuple for each email (mailId, mailBeg)
  maillocs = []
  brkIdx = 0
  frId = 0
  for i in range(len(frlocs)):
    if frlocs[i] > brklocs[brkIdx]: #mail start has crossed a page boundary
      frId = 1 #start renumbering emails at page break
      for j in range(brkIdx + 1,len(brklocs)): #how many page boundaries did we cross?
        if brklocs[j] > frlocs[i]:
          brkIdx = j
          break
    else:
      frId += 1
 
    mailId = str(srcId) + '_' + str(brkIdx + 1) + '_' + str(frId) #adobe reader page numbering starts at 1   
    maillocs.append((mailId,frlocs[i]))

  #now we can create a record for each email from that single big text string
  mails = []
  for i in range(len(maillocs)):
    (mailId,mailBeg) = maillocs[i] #find the beginning and end of each email in the big test string
    if i < len(maillocs) - 1: 
      mailEnd = maillocs[i+1][1]
    else:
      mailEnd = len(txt)
    mailCt += 1
    mails.append(mkMailRec(mailCt,mailId,txt[mailBeg:mailEnd]))

#output results to a file
with open(sys.argv[2] + '.json', 'w') as f:
    json.dump(mails, f)

#output stuff to stdout just for debugging
for mail in mails:
  print('=============')
  print(mail)
  #for key in ['mailNo','mailId','from','to','date','cc','subject','body']:

print('0^^^^^^^^^^^^^^^^^^^^^^')
cols = ['mailId','from','date']
tbl = [cols]
for mail in mails:
  row = []
  for key in cols:
    row.append(mail[key])
  tbl.append(row)
niceTbl =  tabulate(tbl,headers='firstrow')
print(niceTbl)



print('1^^^^^^^^^^^^^^^^^^^^^^')
cols = ['mailId','to','cc']
tbl = [cols]
for mail in mails:
  row = []
  for key in cols:
    row.append(mail[key])
  tbl.append(row)
niceTbl =  tabulate(tbl,headers='firstrow')
print(niceTbl)


print('2^^^^^^^^^^^^^^^^^^^^^^')
for mail in mails:
  print(mail['mailId'],'  !!!!!!!!!!!!!!')
  print(mail['body'])

print('3^^^^^^^^^^^^^^^^^^^^^^')
print('mailCt = ',mailCt,'    pageCt = ',pageCt)

