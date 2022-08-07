import argparse
import re
import json
import csv
import itertools
from pdfminer.high_level import extract_pages
#print(pdfminer.__version__)


def mklines(block):
  pdf_id,pg,x0,x1,y0,y1,text = [x for x in range(7)]

  segs = []
  for elem in block:
    snips = elem[text].split('\n')
    if snips[-1] == '':
      snips = snips[0:-1]
    snip_ct = len(snips)
    snip_y1 = elem[y1]
    snip_ht = (snip_y1 - elem[y0])/snip_ct
    snip_y0 = snip_y1 - snip_ht
    for snip in snips:
      segs.append([elem[pdf_id],elem[pg],elem[x0],elem[x1],snip_y0,snip_y1,snip])
      snip_y1 = snip_y0
      snip_y0 = snip_y1 - snip_ht

  segs.sort(key=lambda row: row[y1],reverse=True)
  lines = []
  line = segs[0]
  for i in range(1,len(segs)):
    seg = segs[i]
    seg_mid = (seg[y1] + seg[y0])/2
    if line[y0] < seg_mid < line[y1]:
      if seg[x0] < line[x0]: 
        line[text] = seg[text] + ' ' + line[text]
        line[x0] = seg[x0]
      else:
        line[text] = line[text] + ' ' + seg[text]
        line[x1] = seg[x1]
    else:
      lines.append(line)
      line = seg
  lines.append(line)
  return lines


def mkblocks(page):
  pdf_id,pg,x0,x1,y0,y1,text = [x for x in range(7)]
  data = page.copy()

  data.sort(key=lambda row: row[y1],reverse=True) #tops of elements from top of page down
  data_ct = len(data)
  blocks = []
  block = []
  cur_y1 = data[0][y1]
  cur_y0 = data[0][y0]
  for elem in data:
    if cur_y0 > elem[y1]: #no y overlap so a whole horizontal line has been assembled 
      blocks.extend(mklines(block))
      block = [elem]
      cur_y1 = elem[y1]
      cur_y0 = elem[y0]
    else:
      block.append(elem)
      if cur_y0 > elem[y0]:
        cur_y0 = elem[y0] #extend the bottom of the block

  blocks.extend(mklines(block))
  return blocks


parser = argparse.ArgumentParser()
parser.add_argument('grp', help='chooses group of files')
parser.add_argument('inf', help='input json file')
parser.add_argument('outf', help='output text json file')
parser.add_argument('dbgf', help='csv debug file')
args = parser.parse_args()
  
with open(args.inf,'r') as inf:
  #hdr,db,pdf_ids = json.load(inf)
  db = json.load(inf)

#################### Issues with pdf to json conversion #######################
# - Text on the same horizontal may be in different elements if the horizontal space between two words is large
# - Text on two different horizontals will be in the same element if the space between lines is small
# - Text on two different pages will never be in the same element
# - Pages are skipped if empty
# - Redactions can cause lines to be broken in separate elements
# - The elements of a redacted paragraph can be out of order
# - I can't fix any of this in pdfminer.six

pages = []
page = None
pg_num = None
pdf_id = None
for elem in db:
  if elem[0] != pdf_id or elem[1] != pg_num:
    pdf_id = elem[0]
    pg_num = elem[1]
    if page != None:
      pages.extend(mkblocks(page))
    page = [elem]
  else:
    page.append(elem)
pages.extend(mkblocks(page))

with open(args.outf,'w') as f:
  json.dump(pages,f,indent=2)

