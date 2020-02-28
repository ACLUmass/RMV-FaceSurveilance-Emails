import sys
import json
import re
import tabulate
import datetime
import time
from nameparser import HumanName

#usage in python3 environment
# python rqMatch.py nodupMails.json allLogs.json > nodupDbg.txt
#filenames must be relative to pdf_processing

#create a database of all emails that include image attachments (pdf,png,jpeg.gif)
#create a database of allLog entries that came in by email
#for each entry in the allLog database try to find an entry in the email database that corresponds to it based on the following
# The person's name who sent the email must be in both databases
# The date in the email must precede the one in the log entry 
# The date in the log entry must be later than the next one from the same person

#1)if the number of images in the email don't match the number in the log, then this is a suspicious email.
#2)any log entries with no matching email are suspicious
#3)any email entries with no matching log are suspicious and have to be processed to see if they have an accompanying rejection email


day = re.compile('Sunday|Monday|Tuesday|Wednesday|Wed nesday|Thursday|Friday|Saturday|Thw\Ssday',re.IGNORECASE) #stupid thrusday typo
typo = re.compile('\dAM$|\dPM$')
typo1 = re.compile('^\s*2019 3:03:00 PM') #another dumbass typo
typo2 = re.compile('^\s*2019 3:42:12 PM')
def str2ts(date):
  if not re.search('\S',date):
    return date
  x = date.replace(u'\xa0',' ')
  if typo1.match(x):
    x = 'August 6, 2019 3:03:00 PM' #another dumbass typo
  if typo2.match(x):
    x = 'August 6, 2019 3:42:12 PM' #another dumbass typo
  x = x.replace(' at ',' ')
  x = x.replace(',','')
  x = x.replace(' CST','') #central standard time doesn't convert and we don't care
  x = day.sub('',x)
  y = x.split()
  x = ' '.join(y)
  if typo.search(x):
    x = x[0:-2] + ' ' + x[-2:]  #insert a space before AM or PM
  x = x.replace(' 2 01:25 ',' 2:01:25 ') #another dumbass typo
  x = x.replace(' 12: 16',' 12:16') #another dumbass typo
  x = x.replace('2:S4','2:54') #another dumbass typo
  x = x.replace('07 :29','07:29') #another dumbass typo
  x = x.replace('3 07 00','3:07:00') #another dumbass typo
  x = x.replace('Octo r','October') #another dumbass typo
  x = x.replace('Dece mber','December') #another dumbass typo
  

  try:
    # ' Friday December 9 2016 10:02:21 AM'
    t = time.mktime(datetime.datetime.strptime(x, "%B %d %Y %H:%M:%S %p").timetuple())
    return int(t)
  except:
    pass
  try:
    # ' Wednesday December 20 2017 11:11 AM'
    t = time.mktime(datetime.datetime.strptime(x, "%B %d %Y %H:%M %p").timetuple())
    return int(t)
  except:
    pass
  try:
    # ' March 11 2017 4:22:43 PM EST'
    t = time.mktime(datetime.datetime.strptime(x, "%B %d %Y %H:%M:%S %p %Z").timetuple())
    return int(t)
  except:
    pass
  try:
    # ' March 11 2017 4:22:43 EST'
    t = time.mktime(datetime.datetime.strptime(x, "%B %d %Y %H:%M:%S %Z").timetuple())
    return int(t)
  except:
    print('-' + x + '-')
    return 1234567890
    #exit()


def nameSplit(name):
  words = name.split()
  if len(words) == 0:
    return '',''
  for i in range(len(words)):
    if not re.search('^[A-Z]',words[i]):
      break
  return ''.join(words[0:i]),''.join(words[i:])

def nameMatch(nameA,nameB):
  properA, routeA = nameSplit(nameA)
  properB, routeB = nameSplit(nameB)
  if len(properA) != 0 and len(properB) != 0:  #if both preaent, they MUST match
    if properA == properB:
      return True
    else:
      return False
  else: #can't compare proper names because at least one is missing so do a fuzzy route match
    if len(routeA) == 0 or len(routeB) == 0: #can't match routes, keep the duplicate
      return False
    ratio = fuzz.ratio(routeA,routeB)
    if ratio > 90:
      return True
    else:
      return False

def dateMatch(dateA,dateB):
  if dateA == None or dateB  == None: #we don't have both dates
    return False
  tmpA = dateA.strip()
  tmpB = dateB.strip()
  if len(tmpA) == 0  or len(tmpB) == 0: #we don't have both dates
    return False
  if tmpA == tmpB:
    return True
  else:
    return False

#build a database of all the emails with images
inf = open(sys.argv[1], 'r')
r = inf.read()  #read in all the bytes into one string
mails = json.loads(r)
mailTot = len(mails)

imgCt = 0
rqCt = 0
#imgChk = re.compile('\S+\.jpeg|\S+\.pdf|\S+\.png|\S+\.gif')
imgChk = re.compile('\.jpeg|\.pdf|\.png|\.gif')
mailHist = {}
mailHistCt = 0
for i in range(mailTot):
  tmp = str(mails[i]['body'])
  tmp = tmp.replace('logo.png','')
  tmp = tmp.replace('lock.gif','')
  if imgChk.search(tmp) != None:
    print('============')
    print(mails[i]['from'])
    print(mails[i]['date'])
    if mails[i]['date']:
      t = str2ts(mails[i]['date'])
      print(t)
    rqCt += 1
    imgs = imgChk.finditer(tmp)
    for img in imgs:
      imgNm = tmp[:img.end()]
      imgCt += 1
      print(imgNm)
    name = HumanName(mails[i]['from'])
    #fullNm = name.first + ' ' + name.last
    #fullNm = fullNm.lower()
    fullNm = name.last.lower()
    if fullNm in mailHist.keys():
      mailHist[fullNm] += 1
    else:
      mailHist[fullNm] = 1
      mailHistCt += 1

print('histCt = =',mailHistCt)

print('#################################')
#build a database of all the logs for email surveillence requests
inl = open(sys.argv[2], 'r')
l = inl.read()  #read in all the bytes into one string
logs = json.loads(l)
logTot = len(logs)

cols = logs[0]
logDb = []
logCt = 0
phoCt = 0
for i in range(1,len(logs)):
  logCt += 1
  log = {}
  for col in cols:
    log[col] = logs[i][cols.index(col)]
  logDb.append(log)

tcol = ['number','date','officer','fullNm','reqMethod','reqNum']
tdb = [tcol]
eRq = 0
logHist = {}
for log in logDb:
  tmp1 = log['reqMethod']
  tmp2 = log['reqNum']
  if re.search('\d+',tmp2):
    phoCt += int(tmp2) 
  if re.search('mail',tmp1) != None:
    if re.match('\(',log['day']): #a couple of special cases
      log['day'] = '6'
    if re.search('/',log['day']):
      log['day'] = '24'
    tmp = log['year'] + '/' + log['month'].strip() + '/' + log['day']
    tmp = time.mktime(datetime.datetime.strptime(tmp, "%Y/%B/%d").timetuple())
    name = HumanName(log['officer'])
    fullNm = name.first + ' ' + name.last
    #fullNm = fullNm.lower()
    fullNm = name.last.lower()
    #row = [log['number'],tmp,log['officer'],tmp1,tmp2]
    row = [log['number'],tmp,log['officer'],fullNm,tmp1,tmp2]
    eRq += 1
    tdb.append(row)
    if fullNm in logHist.keys():
      logHist[fullNm] += 1
    else:
      logHist[fullNm] = 1
  

#for i in range(logTot):
#  print(logs[i])
tbl = tabulate.tabulate(tdb, headers='firstrow',floatfmt='5.2f')
print(tbl)
print('mailTot = ',mailTot,'imgCt = ',imgCt,'rqCt = ',rqCt,'logCt = ',len(logDb),'eRq = ',eRq,'phoCt = ',phoCt)

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
mailCt = 0
mailNmCt = 0
for key in mailHist:
  print(key,mailHist[key])
  mailCt += mailHist[key]
  mailNmCt += 1

print('--------------------------------')
logCt = 0
logNmCt = 0
hitCt = 0
hitList = []
hitTot = 0
for key in logHist:
  print(key,logHist[key])
  logCt += logHist[key]
  logNmCt += 1
  if key in mailHist.keys():
    hitCt += 1
    hitTot += mailHist[key]
    hitList.append(key)

#for record sorting the misslist
def score(elem):
  return elem[1]

missCt = 0
missList = []
for key in mailHist.keys():
  try:
    b = hitList.index(key)
  except:
    missCt += mailHist[key]
    missList.append([key,mailHist[key]])

missList.sort(key=score,reverse=True)

mtbl = [['name','rqs']] + missList
tbl = tabulate.tabulate(mtbl, headers='firstrow')
print(tbl)

print('mailCt = ',mailCt,'mailNmCt = ',mailNmCt,'logCt = ',logCt,'logNmCt = ',logNmCt,'hitCt = ',hitCt,'missCt = ',missCt,'hitTot = ',hitTot )
