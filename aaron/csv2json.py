import sys
import json
 
#sys.argv[1] is a json file (no json extention) of all the log spreadsheets exported in csv form (no csv extension) as follows
#[['year','filename'],....]

#sys.argv[2] is the json file to create without the json extension

logList = open(sys.argv[1] + '.json', 'r')
r = logList.read()  #read in all the bytes into one string
logs = json.loads(r)

#header from rmv is so screwed up that we have ignore its lines in csv and make our own,
tbl = [['number','year','month','day','officer','agency','office','location','reqMethod','reqNum','reqMatch','photoAry','other','notes']]

for log in logs:
  year = log[0]
  infile = log[1]
  inf = open(infile + '.csv','r')
  lines = inf.readlines()
  for  i in range(4,len(lines)):  #skip 4 useless header lines
    line = lines[i].split(',')
    tbl.append([line[0]] + [year] + line[1:])

with open(sys.argv[2] + '.json', 'w') as f:
    json.dump(tbl, f)

