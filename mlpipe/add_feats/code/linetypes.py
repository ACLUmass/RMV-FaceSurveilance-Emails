import argparse
import re
import json
import csv
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

parser = argparse.ArgumentParser()
parser.add_argument('grp', help='chooses group of files')
parser.add_argument('inf', help='input json file')
parser.add_argument('outf', help='output text json file')
parser.add_argument('dbgf', help='csv debug file')
args = parser.parse_args()
  
with open(args.inf,'r') as inf:
  db = json.load(inf)

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
