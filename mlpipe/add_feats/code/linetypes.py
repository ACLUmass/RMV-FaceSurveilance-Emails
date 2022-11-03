import argparse
import re
import json
import csv
from datetime import datetime
from nameparser import HumanName
#print(pdfminer.__version__)
'''
Parse each line and add features
'''

################################### Helper Functions #################################
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

#def mkTimeStamp(yr,mon,day): #mon is month abbreviation or fullname
#  try:
#    mon_num = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(mon[0:3]) + 1
#    #return yr,mon,day
#    return datetime(int(yr),mon_num,int(day)).timestamp()
#  except:
#    return None

def mkTimeStamp(text):
  parts = text.split()
  yr = None
  mon = None
  day = None
  for part in parts:
    #tmp = re.match('\d{4}',part)
    if re.match('\d{4}',part) != None:
      yr = re.match('\d{4}',part).group()
    elif re.match('\d{1,2},',part) != None:
      day = re.match('\d{1,2},',part).group()[0:-1]
    else:
      try:
        mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(part[0:3]) + 1
      except:
        pass
  if yr != None and mon != None and day != None: 
    return datetime(int(yr),mon,int(day)).timestamp()
  return None


############################### main program ##################################
line_types = {}
line_types['from_hdr'] = re.compile('^From:')
line_types['to_hdr'] = re.compile('^To:')
line_types['cc_hdr'] = re.compile('^Cc:')
line_types['date_hdr'] = re.compile('^Date:|Sent:')
line_types['rply_hdr'] = re.compile('^Subject:\s+RE:') #NOTE - must be ahead of subj_hdr
line_types['subj_hdr'] = re.compile('^Subject:')

parser = argparse.ArgumentParser()
parser.add_argument('grp', help='chooses group of files')
parser.add_argument('inf', help='input json file')
parser.add_argument('outf', help='output text json file')
parser.add_argument('dbgf', help='csv debug file')
args = parser.parse_args()

with open(args.inf,'r') as inf:
  db = json.load(inf)

pdf_id,pg,x0,x1,y0,y1,text,lntype = [x for x in range(8)]
pdf_pg = None
pg_doc_ct = 0
doc_id = None
for line in db: #go thru each line of db
  for nm,chk in line_types.items(): #check each line type checker to find a match
    if chk.search(line[text]) != None:
      break

  if nm == 'from_hdr':
    first_nm,sur_nm = getFromNames(line[text])
    tmp = line[pdf_id] + '_' + str(line[pg])
    if tmp != pdf_pg:
      pdf_pg = tmp
      pg_doc_ct = 0
    pg_doc_ct += 1
    doc_id = pdf_pg + '_' + str(pg_doc_ct)
    line.extend([nm,doc_id,[first_nm,sur_nm]])
  elif nm == 'date_hdr':
    ts = mkTimeStamp(line[text]) 
    line.extend([nm,doc_id,ts])
  else: #no line type match, just add a doc_id if it exists
    line.extend([None,doc_id])

with open(args.outf,'w') as f:
  json.dump(db,f,indent=2)

#check header completeness
from_hdr_ct = 0
date_hdr_ct = 0
part_hdrs = []
for line in db:
  if line[lntype] == 'from_hdr':
    from_hdr_ct += 1
    part_hdrs.append([line[8],line[9],line[6]])
  elif line[lntype] == 'date_hdr': 
    date_hdr_ct += 1
    part_hdrs.append([line[8],line[9],line[6]])
	
      
#col_nms = 'pdf,pg,x0,x1,y0,y1,text,lntype,doc_id'
col_nms = 'doc_id,feat,text'
cols = col_nms.split(',') #use as first row of csv output file for column names
col_ct = len(cols)
        
with open(args.dbgf, 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  spamwriter.writerow(cols)
  for row in part_hdrs:
    spamwriter.writerow(row)
  spamwriter.writerow(['total emails',from_hdr_ct,'missing_info',len(part_hdrs)])
