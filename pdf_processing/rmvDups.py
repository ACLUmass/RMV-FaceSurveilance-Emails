import sys
import json
import re
from fuzzywuzzy import fuzz

#usage in python3 environment
# python rmvDups.py allMails.json nodupMails.json > nodupDbg.txt
#filenames must be relative to pdf_processing

#sys.argv[1] is a json file of all the emails
#[['year','filename'],....]

#sys.argv[2] is the json file to create without duplicate emils
#mailDbg.txt is debugging print statements

#Two emails with exactly the same date timestamp almost certainly the same. We will check the From and To people
#If either comparison fails then the duplicate emails will be kept. The body is not checked because there is so
#much redaction and cut and paste that it is hard to pick a threshold of similarity that I'd have confidence in.

# An email name string can be divided into a proper name and a route. Due to redacting and cut and paste,
# the string may if none, one or both of these parts. Also either part may be malformed. 
# The rules of comparison are:
# If two string both contain a proper name, they must match exactly to return True
# If only the routes are present the the Levenshtein distance must be close to return True
# If missing parts make the above comparisons impossible, return False

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

inf = open(sys.argv[1], 'r')
r = inf.read()  #read in all the bytes into one string
mails = json.loads(r)
nodupMails = []
mailTot = len(mails)
dupIds = []
missCt = 0
for i in range(mailTot-1):
  if not i in dupIds: #don't check email that is already identified as duplicate
    tmp = mails[i]
    nodupMails.append(tmp)
    end = i + 100
    if end > mailTot:
      end = mailTot
    for j in range(i+1,end):
      tmp1 = mails[j]
      if dateMatch(tmp['date'],tmp1['date']): #if dates match we consider it a match unless from: or to: contradict
        tmpFrom = tmp['from']
        tmp1From = tmp1['from']
        tmpTo = tmp['to']
        tmp1To = tmp1['to']
        tmp1Id = tmp1['mailId']
        if tmpFrom != None and tmp1From != None: #we have froms to check
          if not nameMatch(tmpFrom,tmp1From):
            missCt += 1 #we got here because date was the only thing that matched, debug this
            print('==================================  ',i)
            print('mailId: ',tmp['mailId'],'date: ',tmp['date'],'from: ',tmp['from'],'to: ',tmp['to'])
            print('body: ',tmp['body'])
            print('--------  ',j)
            print('mailId: ',tmp1['mailId'],'date: ',tmp1['date'],'from: ',tmp1['from'],'to: ',tmp1['to'])
            print('body: ',tmp['body'])
        elif tmpTo != None and tmp1To != None: #we have tos to check
          if not nameMatch(tmpTo,tmp1To):
            missCt += 1 #we got here because date was the only thing that matched, debug this
            print('==================================  ',i)
            print('mailId: ',tmp['mailId'],'date: ',tmp['date'],'from: ',tmp['from'],'to: ',tmp['to'])
            print('body: ',tmp['body'])
            print('--------  ',j)
            print('mailId: ',tmp1['mailId'],'date: ',tmp1['date'],'from: ',tmp1['from'],'to: ',tmp1['to'])
            print('body: ',tmp1['body'])

        dupIds.append(j)

lastId = mailTot - 1
if not lastId  in dupIds: #add the last email if it is not a duplicate
  tmp = mails[lastId]
  nodupMails.append(tmp)

#debugging stats
nodupCt = len(nodupMails)
dupCt = len(dupIds)
print('nodupCt = ',nodupCt,'dupCt = ',dupCt,'totCt = ',nodupCt + dupCt,'missCt = ',missCt)

#output results to a file
with open(sys.argv[2], 'w') as f:
  json.dump(nodupMails, f)

