import argparse
import os
import re
import json
import csv
import pdfminer
import pdfminer.high_level
from pdfminer.high_level import extract_pages
#print(pdfminer.__version__)

#NOTE - I can't manipulate any of these parameters to group lines in two boxes that that are horizontally parallel
#pdfminer.layout.LAParams(line_margin = 25.0)
#pdfminer.layout.LAParams(word_margin = 100.0)
#pdfminer.layout.LAParams(boxes_flow = 0.5)

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='input pdf file directory')
parser.add_argument('grp', help='chooses group of files')
parser.add_argument('outf', help='output text json file')
parser.add_argument('crvf', help='output curve json file')
parser.add_argument('dbgf', help='csv debug file')
parser.add_argument('-f', type= int, help='number of pdf files to include')
args = parser.parse_args()


#input all the pdfs and put them in database order
msp_pdfs = []
fr_pdfs = []
for pdf in os.listdir(args.dir):
  if pdf.endswith('.pdf'):
    num = re.search('\d+',pdf)
    num = int(num.group())
    if re.search('All MSP Emails',pdf):
      msp_pdfs.append([num,pdf])
    else:
      fr_pdfs.append([num,pdf])

fr_pdfs = sorted(fr_pdfs, key=lambda x: x[0])
msp_pdfs = sorted(msp_pdfs, key=lambda x: x[0])
tmp = [['msp' + str(x[0]),x[1]] for x in msp_pdfs]
tmp1 = [['fr' + str(x[0]),x[1]] for x in fr_pdfs]
if args.grp == 'fr':
  pdfs = tmp1
else:
  pdfs = tmp

#extract all the relevant info from each file
text_chk = re.compile('<LTTextBoxHorizontal')
curve_chk = re.compile('<LTCurve')
db = []
crvs = []
pdf_ids = []

pdf_ct = len(pdfs)
if args.f != None:
  pdf_ct = args.f


for pdf in pdfs[0:pdf_ct]:
  pdf_id = str(pdf[0])
  pdf_ids.append(pdf_id)
  prev_index = 0
  pg = 0
  for page_layout in extract_pages(args.dir + pdf[1]):
    pg += 1
    for el in page_layout:
      if text_chk.match(el.__str__()) != None: 
        if el.index <= prev_index:
          prev_index = el.index
        db.append([pdf_id,pg,el.x0,el.x1,el.y0,el.y1,el.get_text()])

      elif curve_chk.match(el.__str__()) != None: 
        crvs.append([pdf_id,pg,el.x0,el.x1,el.y0,el.y1,'+'])


col_nms = 'pdf,pg,x0,x1,y0,y1,text'
cols = col_nms.split(',') #use as first row of csv output file for column names
col_ct = len(cols)
cols_ex = col_nms + ' = [x for x in range(' + str(col_ct) + ')]' #executable string for input program to make variable names 

tbl = [col_nms,db,pdf_ids]
with open(args.outf,'w') as f:
  #json.dump(tbl,f,indent=2)
  json.dump(db,f,indent=2)

tbl = [col_nms,crvs,pdf_ids]
with open(args.crvf,'w') as f:
  #json.dump(tbl,f)
  json.dump(db,f)
        
with open(args.dbgf, 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  spamwriter.writerow(cols)
  for row in db:
    spamwriter.writerow(row)

