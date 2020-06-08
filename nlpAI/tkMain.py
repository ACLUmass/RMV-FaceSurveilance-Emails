#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

#usage> python c_nlpAI.py srcFileNm.json, dstFileNm.json > dbg.txt
#srcFileNm = file containing all the emails to train and test
#dstFileNm = write the results of training and testing if sys.arv[2] exists. Overwrites srcFileNm if same.
import sys
import statsLib as stats
import v_nlpAI as view
import m_nlpAI as model
import c_nlpAI as ctl

#create the view object first because it will be needed in callbacks
outfile = None
aiSz = None
try:
  tmp = sys.argv[2]
  if tmp[0] != '-':
    outfile = tmp
  else:
    aiSz = tmp[1:]
  try:
    tmp = sys.argv[3]
    if tmp[0] != '-':
      outfile = tmp
    else:
      aiSz = tmp[1:]
  except:
    pass
except:
  pass

inf = open(sys.argv[1], 'r', encoding='utf-8')
r = inf.read()  #read in all the bytes into one string
m = model.model(r,aiSz) #infile json
 
v = view.view()
#m = model.model(sys.argv[1],aiSz) #infile json
c = ctl.ctl(v,m)
c.run(c)
if outfile != None: #save the results 
  m.fileSv(outfile)

