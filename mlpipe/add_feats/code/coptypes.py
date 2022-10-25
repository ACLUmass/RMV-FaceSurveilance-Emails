import argparse
from nameparser import HumanName
import re
import json
import csv
from datetime import datetime
'''
Parse each log entry and add features based on content. Reorganize the columns for easier manual inspection and debugging
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


parser = argparse.ArgumentParser()
parser.add_argument('inf0', help='face recognition log json file')
parser.add_argument('outf', help='cops json file')
parser.add_argument('dbgf', help='csv debug file')
args = parser.parse_args()
  
with open(args.inf0,'r') as inf:
  rqs_db = json.load(inf)

#yr,mo,dt,cop,agency,office,gov,rq_type,rq_ct,match_ct,photo_ary,other = [x for x in range(12)]
#The people listed in the request log are not employees of MASS DOT-RMV/Enforcement Services 
#that runs FR software
rq_cops = []
no_date_ct = 0
for rq in rqs_db:
  first_nm,sur_nm = getLogNames(rq[3])
  ts = mkTimeStamp(rq[0],rq[1],rq[2])#for rq_cop in rq_cops: 
  if ts != None:
  #  if first_nm == rq_cop[1] and sur_nm == rq_cop[2]:
  #    break
  #else:
  #  rq_cops.append([rq[3],first_nm,sur_nm] + rq[4:7])
    rq_cops.append([ts,rq[7],first_nm,sur_nm,rq[4],rq[6],rq[0],rq[1],rq[2],rq[3],rq[5],rq[8],rq[9],rq[10],rq[11]])
  else:
    no_date_ct += 1

rq_cops.sort(key=lambda row: row[0])
print('no_date_ct ',no_date_ct)
     
#col_nms = 'cop,1st_nm,2nd_nm,agency,office,gov'
col_nms = 'tm_stmp,rq_type,first,sur_nm,agency,gov,yr,mo,dt,cop,office,gov,rq_ct,match_ct,photo_ary,other'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for row in rq_cops:
    csvwriter.writerow(row)
 
exit()
  
with open(args.inf1,'r') as inf:
  email_db = json.load(inf)

#The people sending emails includes FR requestors and MASS DOT-RMV employees 
email_froms = [[x[6],x[8]] for x in email_db if x[7] == 'from_hdr']

uniq_email_froms = []
for email_from in email_froms:
  first_nm,sur_nm = getFromNames(email_from[0])
  for uniq_email_from in uniq_email_froms: 
    if first_nm == uniq_email_from[2] and sur_nm == uniq_email_from[3]:
      break
  else:
    uniq_email_froms.append([email_from[0],email_from[1],first_nm,sur_nm])

     
'''
col_nms = 'cop,email_id,first_nm,sur_nm'
        
with open(args.dbgf, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',')
  csvwriter.writerow(col_nms.split(','))
  for row in uniq_email_froms:
    csvwriter.writerow(row)
 
exit()
'''
 
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
