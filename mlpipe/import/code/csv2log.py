import argparse
import os
import re
import json
import csv


parser = argparse.ArgumentParser()
parser.add_argument('dir', help='input csv file directory')
parser.add_argument('outf', help='output text json file')
parser.add_argument('dbgf', help='csv debug file')
parser.add_argument('-f', type= int, help='number of csv files to include')
args = parser.parse_args()

#input all the csvs and put them in database order
log_csvs = []
for log in os.listdir(args.dir):
  if log.endswith('.csv'):
    yr = re.search('\d{4}',log)
    yr = int(yr.group())
    log_csvs.append([yr,log])
log_csvs = sorted(log_csvs, key=lambda x: x[0])

csv_ct = len(log_csvs)
if args.f != None:
  csv_ct = args.f

logs_db = []
for i in range(csv_ct):
  yr,inf = log_csvs[i]
  with open(args.dir + inf, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
      if re.match('\d+',row[0]):
        row = [None if item == '' else item for item in row]
        day = re.match('\d{1,2}',row[2])
        if day != None:
          day = day.group()
        tmp = [yr,row[1],day]
        tmp.extend(row[3:])
        logs_db.append(tmp)


with open(args.outf,'w') as f:
  json.dump(logs_db,f,indent=2)


