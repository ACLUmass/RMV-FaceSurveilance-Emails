import argparse
from nameparser import HumanName
import re
import json
import csv
from datetime import datetime
'''
Parse each log entry and add features based on content. Reorganize the columns for easier manual inspection and debugging
'''
############################### helper functions ##################################

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

def mkTimeStamp(yr,mon,day): #mon is month abbreviation or fullname
  try:
    mon_num = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(mon[0:3]) + 1
    #return yr,mon,day
    return datetime(int(yr),mon_num,int(day)).timestamp()
  except:
    return None

############################### main program ##################################

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

with open(args.outf,'w') as f:
  json.dump(rq_cops,f,indent=2)

 
