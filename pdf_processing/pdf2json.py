import sys
import re
import json
import pdfplumber
from tabulate import tabulate


#usage in python3 environment
# python pdf2json.py mailList.json allMails.json >mailDbg.txt

#sys.argv[1] is a json file of all the email pdfs
#[['year','filename'],....]
#filename must be relative to pdf_processing

#sys.argv[2] is the json file to create contining all the emails as text
#mailDbg.txt is debugging print statements


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
  #for key in ['from','to','date','sent','cc']:
  for key in ['from','to','date','cc']:
    for i in range(len(lines)):
      #chk = re.match('\s*' + key + ':',lines[i],re.IGNORECASE)
      if key == 'date': 
        chk = re.match('>*\s*' + key + ':',lines[i],re.IGNORECASE)
        chk = re.match('>*\s*(date|sent):',lines[i],re.IGNORECASE)
      else:
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

  if len(lines) > 0:
    email['body'] = ''.join(lines) #what's left is the body
  else:
    email['body'] =  None

  #98% of the emails are well formed enough to be parsed by the code above.
  #The remaining 2% are special cases that we'll try to catch below.

  #case msp3_163_4,5 and others. Multiple fields appear on same line with From:
  if email['date'] == None:  #can't split this email into lines
    email = mkOneLine(mailNo,mailId,txt) #TODO - not perfect. because of mailto: I'm not testing for To:
 
  #msp3_242_2 and ones like it can't be fixed because somebody retyped the info without the identifying header stuff
  #msp3 all other missing fields have been redacted or heading has been omitted
  #fr3_29_2 is screwed up by pdfplumber. It gets the page breaks in the wrong place and finditer misses a from: fr5_10_2 and fr6_146_2 have the same problem
     
  return email

      
#make an email record from the single text string of that email
def mkOneLine(mailNo,mailId,txt):
  email = {}
  email['mailNo'] = mailNo #useful for debugger breakpoints
  email['mailId'] = mailId #useful for locating email in pdf
  hdrlocs = []
  hdrlocs.append((re.search('^From:',txt,re.IGNORECASE).span(),'from')) #these 3 must exist or the email is malformed

  email['to'] = None #these may not exist in email
  email['cc'] = None
  email['body'] = None
  email['date'] = None
  tmp = re.search('Date:|Sent:',txt,re.IGNORECASE)
  if tmp:
    hdrlocs.append((tmp.span(),'date'))
  tmp = re.search('[^l]To:',txt,re.IGNORECASE)
  if tmp:
    hdrlocs.append((tmp.span(),'to'))
  tmp = re.search('Cc:',txt,re.IGNORECASE)
  if tmp:
    hdrlocs.append((tmp.span(),'cc'))

  hdrlocs = sorted(hdrlocs, key=lambda hdr: hdr[0][0]) #now we have the headers fields in the order they occur in text string
  for i in range(len(hdrlocs)):
    key = hdrlocs[i][1]
    datBeg = hdrlocs[i][0][1] #text begins after the key
    if i < len(hdrlocs) - 1: 
      datEnd = hdrlocs[i+1][0][0] #text ends before the next key
    else:
      datEnd = len(txt) #all the rest of the text
    email[key] = txt[datBeg:datEnd]

  #It gets a little tricky here because the email body still has to be separated from the last header parameter
  #I think return is always a separator but I'm not 100% sure.
  key = hdrlocs[-1][1]  #last header
  tmp = re.search('\n',email[key],re.IGNORECASE)
  if tmp:
    div = tmp.span()[1]
    email['body'] = email[key][div:] #everything after the match
    email[key] = email[key][0:div] #everything before the body

  if re.search('.+\n.+',email['from']) != None: #TODO - check why I can't do this on every line
    tmp1 = email['from']
    email['from'] = tmp1.replace('\n',' ')

  return email
 
 
#sys.argv[1] is a json file (no json extention) of all the mail pdfs
#[['prefix','filename'],....]

#sys.argv[2] is the json file to create without the json extension

mailTot = [] #all the emails in all the files for json output
dbgInfo = [] #a tuple for each file (prefix,mailCt,pageCt,blankCt)
mailNo = 0

mailList = open(sys.argv[1], 'r')
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

  #count blank pages
  blankCt = 0
  brkSv = None
  for brk in brklocs:
    if brkSv == None: #find the first page break
      brkSv = brk
    else: #two consecutive page breaks means there is a blank page
      if brk == brkSv + 1:
        blankCt += 1
      brkSv = brk


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
 
    #mailId = str(srcId) + '_' + str(brkIdx + 1) + '_' + str(frId) #adobe reader page numbering starts at 1   
    mailId = srcId + '_' + str(brkIdx + 1) + '_' + str(frId) #adobe reader page numbering starts at 1   
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
    mailNo += 1
    #mails.append(mkMailRec(mailCt,mailId,txt[mailBeg:mailEnd]))
    mails.append(mkMailRec(mailNo,mailId,txt[mailBeg:mailEnd]))

  mailTot.extend(mails)
  #dbgInfo.append((str(srcId),mailCt,pageCt))
  dbgInfo.append((srcId,mailCt,pageCt,blankCt))

#output results to a file
with open(sys.argv[2], 'w') as f:
    #json.dump(mails, f)
    json.dump(mailTot, f)

#output stuff to stdout just for debugging
#for mail in mails:
for mail in mailTot:
  print('=============')
  print(mail)
  #for key in ['mailNo','mailId','from','to','date','cc','subject','body']:

print('0^^^^^^^^^^^^^^^^^^^^^^')
cols = ['mailId','from','date']
tbl = [cols]
#for mail in mails:
for mail in mailTot:
  row = []
  for key in cols:
    row.append(mail[key])
  tbl.append(row)
niceTbl =  tabulate(tbl,headers='firstrow')
print(niceTbl)



print('1^^^^^^^^^^^^^^^^^^^^^^')
cols = ['mailId','to','cc']
tbl = [cols]
#for mail in mails:
for mail in mailTot:
  row = []
  for key in cols:
    row.append(mail[key])
  tbl.append(row)
niceTbl =  tabulate(tbl,headers='firstrow')
print(niceTbl)


print('2^^^^^^^^^^^^^^^^^^^^^^')
#for mail in mails:
for mail in mailTot:
  print(mail['mailId'],'  !!!!!!!!!!!!!!')
  print(mail['body'])

print('3^^^^^^^^^^^^^^^^^^^^^^')
mailCtTot = 0
pageCtTot = 0
blankCtTot = 0
for dbg in dbgInfo:
  mailCtTot += dbg[1]
  pageCtTot += dbg[2]
  blankCtTot += dbg[3]
  print('srcId = ',dbg[0],'   mailCt = ',dbg[1],'   pageCt = ',dbg[2],'   blankCt = ',dbg[3])


pageAvg = float(mailCtTot/(pageCtTot - blankCtTot)) # average number of emails in non blank pages
mailMiss = pageAvg * blankCtTot #assume the same average for blank pages

print('mailCtTot = ',mailCtTot,'   pageCtTot = ',pageCtTot,'   blankCtTot = ',blankCtTot,'   est. missed emails = ',mailMiss)
