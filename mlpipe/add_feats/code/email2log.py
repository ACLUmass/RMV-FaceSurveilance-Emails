import argparse
from nameparser import HumanName
import re
import json
from datetime import datetime
import csv
'''
from pdfminer.high_level import extract_pages
#print(pdfminer.__version__)

pdf_id,pg,x0,x1,y0,y1,text,lntype = [x for x in range(8)]
line_types = {}
line_types['from_hdr'] = re.compile('^From:')
line_types['to_hdr'] = re.compile('^To:')
line_types['cc_hdr'] = re.compile('^Cc:')
line_types['date_hdr'] = re.compile('^Date:|Sent:')
line_types['rply_hdr'] = re.compile('^Subject:\s+RE:') #NOTE - must be ahead of subj_hdr
line_types['subj_hdr'] = re.compile('^Subject:')
'''
def parseName(text):
  name = HumanName(text)
  sur_nm = name.last
  if sur_nm == '':
    sur_nm = name.first
    #fst_nm = None
    fst_nm = ''
  else:
    fst_nm = name.first
  return fst_nm,sur_nm

def getLogNames(text):
  p = re.compile('Deportation\sOffice|[aA]gent|special|Inspector|Patrolman|\sfor\sICE\s|\sfor\s|H\.O\.|H\.O|P\.O')
  tmp = p.sub(' ',text)
  tmp = tmp.replace('"',' ')
  tmp = ' '.join(tmp.split('/'))
  title = re.match('[A-Z]+\s|\w{2,}\.',tmp)
  if title != None:
    tmp = tmp[title.end():]
  return parseName(tmp)

def getFromNames(text):
  r = re.compile('"')
  tmp = r.sub(' ',text)
  p = re.match('From:',tmp)
  tmp = tmp[p.end():]
  q = re.search('\(|\[|\]|<|@',tmp)
  if q != None:
    tmp = tmp[0:q.start()]
  s = re.compile('\.')
  tmp = s.sub(' ',tmp)
  return parseName(tmp)

def mkTimeStamp(yr,mon,day): #mon is month abbreviation or fullname
  try:
    mon_num = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(mon[0:3]) + 1
    #return yr,mon,day
    return datetime(int(yr),mon_num,int(day)).timestamp()
  except:
    return None

def getEmailDate(text):
  tmp = re.search('\d{4}',text)
  if tmp == None:
    #return None,None,None
    return None
  yr = tmp.group()
  tmp1 = re.search('\d{1,2}',text[0:tmp.start()])
  if tmp1 == None:
    return None
  day = tmp1.group()
  tmp2 = text[0:tmp1.start()].split()
  return mkTimeStamp(yr,tmp2[-1],day)
  #try:
  #  mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(tmp2[-1][0:3]) + 1
  #  #return yr,mon,day
  #  return datetime(yr,mon,day).timestamp()
  #except:
  #  return None

  #this routine is hand created from looking at the names in the log. It includes nicknames
  #and spelling corrections
def first_nm_eq(nm0,nm1):
  sames = [['Anthony','Tony'],
           ['Susan','Sue'],
           ['Jamie','Jaime'],
           ['Stephen','Stepher'],
           ['Timothy','Tim'],
           ['Joao','Jogo'],
           ['Michael','Mike'],
           ['Robert','Bobby'],
           ['Benjamin','Ben']]

  for same in sames:
    if nm0 in same and nm1 in same:
      return True
  if nm0 == nm1:
    return True
  return False
  
parser = argparse.ArgumentParser()
parser.add_argument('grp', help='chooses group of files')
parser.add_argument('inf0', help='face recognition log json file')
parser.add_argument('inf1', help='email json file')
parser.add_argument('outf', help='cops json file')
parser.add_argument('outf1', help='froms json file')
parser.add_argument('dbgf', help='csv debug file')
args = parser.parse_args()
  
with open(args.inf0,'r') as inf:
  rqs_db = json.load(inf)

#yr,mo,dt,cop,agency,office,gov,rq_type,rq_ct,match_ct,photo_ary,other = [x for x in range(12)]
#The people listed in the request log are not employees of MASS DOT-RMV/Enforcement Services 
#that runs FR software
rq_cops = []
for rq in rqs_db:
  first_nm,sur_nm = getLogNames(rq[3])
  time_stamp = mkTimeStamp(rq[0],rq[1],rq[2])
  if time_stamp != None:
    rq_cops.append([rq[0],rq[1],rq[2],rq[3],first_nm,sur_nm] + rq[4:8] + [time_stamp])

rq_cops.sort(key=lambda row: row[-1])

sur_nm_db = {}
for rq_cop in rq_cops:
  sur_nm = rq_cop[5]
  first_nm = rq_cop[4]
  if sur_nm in sur_nm_db:
    if first_nm != '':
      if not first_nm in sur_nm_db[sur_nm]: 
        sur_nm_db[sur_nm].append(first_nm)
  else:
    if first_nm != '':
      sur_nm_db[sur_nm] = [rq_cop[4]]
  
sur_nm_dups = {}
for sur_nm,firsts in sur_nm_db.items():
  if len(firsts) > 1:
    sur_nm_dups[sur_nm] = firsts

#for sur_nm,firsts in sur_nm_dups.items():
#  print(sur_nm,firsts)

with open(args.inf1,'r') as inf:
  email_db = json.load(inf)
 
#from,email_id,first_nm,sur_nm,date,time_stamp
emails_info = []
email_info = None
for email in email_db:
  if email[7] == 'from_hdr':
    first_nm,sur_nm = getFromNames(email[6])
    email_info = [email[6],email[8],first_nm,sur_nm]
  elif email[7] == 'date_hdr':
    if email_info != None:
      date = getEmailDate(email[6])
      if date != None:
        email_info.extend([email[6],date])
        emails_info.append(email_info)
      email_info = None

emails_info.sort(key=lambda row: row[-1])
with open(args.outf1,'w') as f:
  json.dump(emails_info,f,indent=2)


for rq_cop in rq_cops:
  if rq_cop[5] != None:
    for email_info in emails_info:
      if rq_cop[-1] == email_info[-1]:
        if rq_cop[5] == email_info[3]:
          if rq_cop[4] == None or email_info[2] == None or first_nm_eq(rq_cop[4],email_info[2]) == True:
            rq_cop.append(email_info[1])
            break
     
col_nms = 'yr,mon,day,cop,1st_nm,2nd_nm,agency,office,gov,type,time_stamp,rq_id'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for row in rq_cops:
    csvwriter.writerow(row)

exit()

col_nms = 'cop,email_id,first_nm,sur_nm,date,year,month,day'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for row in emails_info:
    csvwriter.writerow(row)
 
exit()
 
#Removing known FR requestors and MASS-DOT_RMV employees from the email senders should show us
#the FR email requests that were omitted from the log
not_rq_cops = []
for uniq_email_from in uniq_email_froms:
  for uniq_rq_cop in uniq_rq_cops:
    if uniq_rq_cop[1] == uniq_email_from[2] and uniq_rq_cop[2] == uniq_email_from[3]:
      break
  else:
    not_rq_cops.append(uniq_email_from)

col_nms = 'cop,email_id,first_nm,sur_nm'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for row in not_rq_cops:
    csvwriter.writerow(row)
exit()
     
col_nms = 'cop,1st_nm,2nd_nm,agency,office,gov'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for cop,dat in rq_cops.items():
    csvwriter.writerow([cop] + dat)
  
exit()
pdf_pg = None
pg_doc_ct = 0
for line in db:
  for nm,chk in line_types.items():
    if chk.search(line[text]) != None:
      if nm == 'from_hdr':
        tmp = line[pdf_id] + '_' + str(line[pg])
        if tmp != pdf_pg:
          pdf_pg = tmp
          pg_doc_ct = 0
        pg_doc_ct += 1
        doc_id = pdf_pg + '_' + str(pg_doc_ct)
      #line.append(nm)
      line.extend([nm,doc_id])
      break
  else:
    try:
      doc_id
    except:
      doc_id = None
    #line.append(None)
    line.extend([None,doc_id])

with open(args.outf,'w') as f:
  json.dump(db,f,indent=2)

#check header completeness
part_hdrs = []
from_hdr_ct = 0
saved_hdr = None
lines_ct = 1
for line in db:
  if line[lntype] == 'from_hdr':
    from_hdr_ct += 1
    if saved_hdr != None:
      if lines_ct < 4:
        part_hdrs.append(saved_hdr)
    saved_hdr = line
    lines_ct = 1
  elif line[lntype] == 'to_hdr': 
    lines_ct += 1
  elif line[lntype] == 'date_hdr': 
    lines_ct += 1
  elif line[lntype] == 'subj_hdr' or line[lntype] == 'rply_hdr': 
    lines_ct += 1
      
col_nms = 'pdf,pg,x0,x1,y0,y1,text,lntype,doc_id'
cols = col_nms.split(',') #use as first row of csv output file for column names
col_ct = len(cols)
        
with open(args.dbgf, 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  spamwriter.writerow(cols)
  for row in part_hdrs:
    spamwriter.writerow(row)
  spamwriter.writerow(['total emails',from_hdr_ct,'missing_info',len(part_hdrs)])
