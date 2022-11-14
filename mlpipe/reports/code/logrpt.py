# vim: set ts=2 sts=0 sw=2 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:

from fpdf import FPDF
from fpdf import enums
import json
import argparse
import logging as logr
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statistics
import re

#{{{ pdf class code
############################### pdf class code #############################
class PDF(FPDF):
  def doc_title(self,title, author,rev):
    self.sec_num = 0
    self.add_page()
    self.set_fill_color(255, 255, 255)
    self.set_font('helvetica', 'B', 25)
    w = self.get_string_width(title) + 6
    self.set_x((210 - w) / 2)
    self.cell(w, 9, title, 0, new_x=enums.XPos.LMARGIN,new_y=enums.YPos.NEXT)
    self.ln(2)
    self.set_font('', 'B', 12)
    self.cell(0, 6, '%s - Rev %s' % (author,rev),0,new_x=enums.XPos.LMARGIN,new_y=enums.YPos.NEXT,align="C")
    self.ln(5)

  def section_title(self, label):
    self.sec_num += 1
    self.ln(5)
    self.set_font('', 'B', 16)
    self.cell(0, 6, 'Section %d: %s' % (self.sec_num, label), 0, new_x=enums.XPos.LMARGIN,new_y=enums.YPos.NEXT)
    self.ln(1)

  def add_image(self, file_nm):
    self.image(file_nm, w=200)
    self.ln(2)

  def add_text(self, text):
    self.set_font('', '', 12)
    self.multi_cell(0, 5, text)
    self.ln()

  def add_note(self, text):
    self.set_font('', 'B', 12)
    self.cell(0,5,'NOTE: ')
    self.ln()
    self.set_font('', '', 12)
    self.multi_cell(0, 5, text)
    self.ln()

  def page_break(self):
    self.add_page()

  def basic_table(self,name, tbl):
    self.set_font('', 'B', 14)
    self.cell(0, 6, 'Table: %s' % (name),0,new_x=enums.XPos.LMARGIN,new_y=enums.YPos.NEXT)
    self.ln(2)

    #find width for each column
    trans_tbl =[[row[i] for row in tbl] for i in range(len(tbl[0]))] #Note: can't use numpy transpose
    col_widths = []
    for col in trans_tbl:
      width = 0
      for dat in col:
        if isinstance(dat,int):
          dat = str(dat)
        elif isinstance(dat,float):
          dat = "{0:.2f}".format(dat)
        w = self.get_string_width(dat) + 6
        if w > width:
          width = w
      col_widths.append(width)

    self.set_font('', 'B', 12)
    headings = tbl[0]
    for idx,heading in enumerate(headings):
      self.cell(col_widths[idx], 7, heading, 1, align="C")
    self.ln()
    self.set_font('', '', 12)

    rows = tbl[1:]
    for row in rows:
      for idx,col in enumerate(row):
        if isinstance(col,int):
          dat = str(col)
        elif isinstance(col,float):
          dat = "{0:.2f}".format(col)
        else:
          dat = col
        self.cell(col_widths[idx], 6, dat, 1)
      self.ln()
#}}}
#{{{ helper functions
############################### helper functions ###########################
def rqMeth(text):
  #order matters because there will be entries with multiple matches and the first is highest priority
  rq_meths = {}
  rq_meths['email'] = re.compile('email')
  rq_meths['walkin'] = re.compile('walkin')
  rq_meths['fax'] = re.compile('fax')
  rq_meths['phone'] = re.compile('phone')

  if text == None:
    return None
  tmp = text.lower()
  tmp = tmp.replace('-','')
  for nm,chk in rq_meths.items():
    if chk.search(tmp) != None:
      return nm
  return None

def rqAgency(gov_lev,agency):
  if gov_lev == None:
    return None,None
  if re.match('Out',gov_lev) != None: #Only out of state agencies with more than one hit are named
    if agency == None:
      return 'OOS_Loc',None
    if re.match('N\.Y\.P\.D',agency) != None:
      return 'OOS_Loc','NYPD' 
    elif re.match('Woonsocket',agency) != None:
      return 'OOS','Woonsocket_RI' 
    else:
      return 'OOS','various'
  elif re.match('Combined',gov_lev) != None:
    return 'combined','various'
  elif re.match('Federal|State|Local',gov_lev) != None:
    tmp = re.match('Federal|State|Local',gov_lev).group()
    return tmp,agency
  else: 
    return None,None
  

# "Gang Affilations and Verifications" is the most reliable section of the report supplies pts.
# cats is the person summary at the end of most most records in the pdfs and it is the more reliable
# than dets but it does not always exist. cats supplies ver_pts. dets is the verification report detail
# section every report but extraction is less reliable than cats. Here are the rules for extraction
# - Extraction returns None if pts does not exist
# - if none of ver_pts cat_sum or det_sum matchs pts return points but no catagories
# - Returning valid catagories depends on which sum matchs pts as follows
#   cat_sum  det_sum  ver_pts   valid catagories
#      Y        x        x        cats 
#      N        Y        x        dets 
#      N        N        x        None 
def get_gang_crits(gang):
  pts = int(gang.get('pts'))
  ver_pts = gang.get('ver_pts')
  cat_sum = gang.get('cat_sum')
  det_sum = gang.get('det_sum')
  cats = gang.get('cats')
  dets = gang.get('dets')
  if pts == None:
    return None,None
  if cat_sum != None and cat_sum == pts:
  #if cat_sum != None:
    return pts,cats
  if det_sum != None and det_sum == pts:
  #if det_sum != None:
    return pts,dets
  return pts,None 


score_cats = { #weak,points, per_incident, text
  'prior_val':[False,9,False,'Prior Validation by a Law Enforcement Agency'],
  'info_law':[False,8,False,'Information Received from an Unaffiliated Law Enforcement Agency'],
  'self_admit':[False,8,False,'Self Admission'],
  'grp_para':[True,4,False,'Use and or Possession of Group Paraphernalia or Identifiers'],
  'grp_photo':[True,2,False,'Group Related Photograph'],
  'grp_tat':[False,8,False,'Known Group Tattoo or Marking'],
  'info_rel':[False,5,False,'Information from Reliable, Confidential Informant'],
  'info_anon':[True,1,False,'Information from Anonymous Informant or Tipster'],
  'rival_grp_cust':[False,3,False,'Victim/Target Affiliated with Member of Rival Group'],
  'rival_grp_no_cust':[False,8,False,'Victim/Target Affiliated with Member of Rival Group'],
  'possess_docs_cust':[False,4,False,'Possession of Documents'],
  'possess_docs_no_cust':[False,8,False,'Possession of Documents'],
  'named_docs':[False,8,False,'Named in Documents as a Member'],
  'possess_pubs':[False,2,False,'Possession of Gang Publications'],
  'partic_pubs':[False,8,False,'Participation in Publications'],
  'court_docs':[False,9,False,'Court and Investigative Documents'],
  'news_accts':[True,1,False,'Published News Accounts'],
  'contact_gang':[False,2,True,'Contact with Known Gang Member/Associate (per interaction)'],
  'bpd_rpt':[False,4,True,'DOCUMENTED ASSOCIATION - BPD 1.1/Incident Report (per interaction)'],
  'member_docs':[False,9,False,'Membership Documents (9 points)'],
  'info_invest':[False,5,False,'Information Developed During Investigation and/or Surveillance'],
  'info_other':[True,1,False,'Information Not Covered By Other Selection Criteria']
}

def per_wks(beg_wks,fin_wks):
  mon,day,yr = beg_wks.split('/')
  beg = datetime.datetime(int(yr),int(mon),int(day))
  mon,day,yr = fin_wks.split('/')
  fin = datetime.datetime(int(yr),int(mon),int(day))
  per = fin - beg
  days = per.days
  if days == 0: #same day begin and end is one day
    days = 1
  return days/7


flag_wds = {}
flag_wds['homicide'] = ['homicide','fatal','murder','kill','death','deceased']
flag_wds['guns'] = ['firearm','gun','shoot','shot','armed','fired','ordinance','ammunition']
flag_wds['weapon'] = ['knives','knife','machete','weapon','blade']
flag_wds['violence'] = ['fought','fight','assault','stabbed','stabbing','altercation','knuckle','kidnap']
flag_wds['threats'] = ['threat','taunt']
flag_wds['drugs'] = ['drug','heroin','marijuana','cocaine','coke','overdose']
flag_wds['arrest'] = ['arrest','warrant']
flag_wds['robbery'] = ['robbery','robbed','steal','stole','carjack','burglar']
flag_wds['damage'] = ['damage','wreck','vandal']
flag_wds['online'] = ['facebook','online','twitter']
violent_flags = ['homicide','gun','weapon','violence','threats']
#}}}
#{{{ plotting functions
############################# plotting functions ###########################

def scatter_plot(x,y,info):
  fig, ax = plt.subplots()
  ax.set_title(info['title'])
  ax.set_xlabel(info['xlabel'])
  ax.set_ylabel(info['ylabel'])

  #rects1 = ax.plot(x, y)
  rects1 = ax.scatter(x, y, s=6.0)
  line = info.get('line')
  if line != None:
    ax.plot([line[0],line[1]],[line[2],line[3]],color = 'black') #[x0,x1],[y0,y1]
    #ax.plot(x,line[0]*x + line[1],color = 'black') #[x0,x1],[y0,y1]

  fig.tight_layout()
  plt.savefig(info['file_nm'])
  plt.show(block=False)

def one_bar_plot(x,y,info):
  fig, ax = plt.subplots()
  ax.set_title(info['title'])
  ax.set_xlabel(info['xlabel'])
  ax.set_ylabel(info['ylabel'])

  width = 0.70  # the width of the bars
  rects1 = ax.bar(x, y, width)

  fig.tight_layout()
  plt.savefig(info['file_nm'])
  #plt.show(block=False)

def two_bar_plot(x,y1,y2,info):
  fig, ax = plt.subplots()
  ax.set_title(info['title'])
  ax.set_xlabel(info['xlabel'])
  ax.set_ylabel(info['ylabel'])

  width = 0.45  # the width of the bars
  rects1 = ax.bar(x - width/2, y1, width, label = info['y1legend'])
  rects2 = ax.bar(x + width/2, y2, width, label = info['y2legend'])
  ax.legend()

  fig.tight_layout()
  plt.savefig(info['file_nm'])
  #plt.show(block=False)
#}}}
############################### main program ###############################
parser = argparse.ArgumentParser()
parser.add_argument('inf', help='input json of fr requests')
parser.add_argument('outf', help='output report')
parser.add_argument('logf', help='output logger text')
args = parser.parse_args()

logr.basicConfig(filename=args.logf, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#record columns = tm_stmp,rq_meth,first,sur_nm,agency,gov,rq_ct,match_ct,yr,mo,dt,cop,office,gov,rq_ct,match_ct,photo_ary,other
with open(args.inf,'r') as inf:
  db = json.load(inf)

pdf = PDF()
pdf.doc_title('RMV Face Recognition Statistics','Aaron Boxer','1.0')

#{{{ log statistics
############################### collect log statistics #####################
intro_text = '''
The database used to generate this report was created from RMV Enforcement Charts from 2016 through August of 2019 and a redacted record of emails pertaining to Face Recognition activity by the MSP.
'''
pdf.add_text(intro_text)

tm_stamp,rq_meth,first_nm,sur_nm,agency,gov_lev,rq_ct,match_ct = [x for x in range(8)]
agency_hits = {}
rqs_db = []
for rec in db:
  tmp = rec[agency]
  tmp1,tmp2 = rqAgency(rec[gov_lev],rec[agency])
  rqs_db.append([rec[tm_stamp],rqMeth(rec[rq_meth]),tmp1,tmp2,rec[first_nm],rec[sur_nm]])
  if tmp in agency_hits:
    agency_hits[tmp] += 1
  else:
    agency_hits[tmp] = 1

agencies = [(key, value) for key, value in agency_hits.items()]
agencies.sort(key=lambda x: x[-1],reverse=True)

rqs_sz = len(rqs_db)
email_rqs = [x for x in rqs_db if x[1] == 'email']
email_sz = len(email_rqs)
walkin_rqs = [x for x in rqs_db if x[1] == 'walkin']
walkin_sz = len(walkin_rqs)
fax_rqs = [x for x in rqs_db if x[1] == 'fax']
fax_sz = len(fax_rqs)
phone_rqs = [x for x in rqs_db if x[1] == 'phone']
phone_sz = len(phone_rqs)
none_rqs = [x for x in rqs_db if x[1] == None]
none_sz = len(none_rqs)

if rqs_sz != email_sz + walkin_sz + fax_sz + phone_sz + none_sz:
  print(rqs_sz,email_sz,walkin_sz,fax_sz,phone_sz,none_sz)

fed_rqs = [x for x in rqs_db if x[2] == 'Federal']
fed_sz = len(fed_rqs)
state_rqs = [x for x in rqs_db if x[2] == 'State']
state_sz= len(state_rqs)
local_rqs = [x for x in rqs_db if x[2] == 'Local']
local_sz= len(local_rqs)
comb_rqs = [x for x in rqs_db if x[2] == 'combined']
comb_sz= len(comb_rqs)
unk_rqs = [x for x in rqs_db if x[2] == None]
unk_sz= len(unk_rqs)
oos_rqs = [x for x in rqs_db if x[2] != None and re.match('OOS',x[2]) != None]
oos_sz= len(oos_rqs)

if rqs_sz != fed_sz + state_sz + local_sz + comb_sz + unk_sz + oos_sz:
  print(rqs_sz,fed_sz,state_sz,local_sz,comb_sz,unk_sz,oos_sz)

in_state_hits = {}
for rq in state_rqs:
  if rq[3] in in_state_hits:
    in_state_hits[rq[3]][1] += 1 
  else:
    in_state_hits[rq[3]] = ['state',1] 

for rq in local_rqs:
  if rq[3] in in_state_hits:
    in_state_hits[rq[3]][1] += 1 
  else:
    in_state_hits[rq[3]] = ['local',1] 

in_state_agencies = [(key, value) for key, value in in_state_hits.items()]
in_state_agencies.sort(key=lambda x: x[-1][-1],reverse=True)


pdf.section_title('Who Made Face Recognition Requests and How')
gov_text = '''
The RMV receives face recognition requests from lots of different agencies at several different govermental levels. The table below shows a breakdown of those levels. Over 70% were from in-state agencies and about 20% were from the federal government.
'''
pdf.add_text(gov_text)

tbl = [['Gov. Level','fraction','count'],
      ['state',state_sz/rqs_sz,state_sz],
      ['local',local_sz/rqs_sz,local_sz],
      ['federal',fed_sz/rqs_sz,fed_sz],
      ['out of state',oos_sz/rqs_sz,oos_sz],
      ['several',comb_sz/rqs_sz,comb_sz],
      ['none',unk_sz/rqs_sz,unk_sz],
      ['total',rqs_sz/rqs_sz,rqs_sz]]
pdf.basic_table('Goverment Levels',tbl)
pdf.add_note('Only a couple of log entries did not list the government level and were counted as "none"')

in_state_text =='''
Since in-state requests are over 70$ of the total it is interesting to know which agencies made most of them. The table below shows this breakdown.
'''


meth_text = '''
There are several ways face recognition requests are made to the RMV as the table below shows. Most of them are email requests so if the log is accurate then we should be able to find those emails in the 8 MSP Email pdfs we were given. The table below shows all ways requests were made.
'''
pdf.add_text(meth_text)

tbl = [['Method','fraction','count'],
      ['email',email_sz/rqs_sz,email_sz],
      ['walkin',walkin_sz/rqs_sz,walkin_sz],
      ['fax',fax_sz/rqs_sz,fax_sz],
      ['phone',phone_sz/rqs_sz,phone_sz],
      ['none',none_sz/rqs_sz,none_sz],
      ['total',rqs_sz/rqs_sz,rqs_sz]]
pdf.basic_table('Request Methods',tbl)
pdf.add_note('A significant number of log entries did not list the method and were counted as "none"')


#}}}

pdf.output(args.outf)
exit()

#{{{ collect living records
############################### collect living records #####################
live_recs = []
total_recs_ct = 0
act_recs_ct = 0
inact_recs_ct = 0
incarc_recs_ct = 0
dead_recs_ct = 0
for rec in db.keys():
  total_recs_ct += 1
  status = db[rec].get('act')
  if status == 'DECEASED':
    dead_recs_ct += 1
  else:
    live_recs.append(db.get(rec))
    if status == 'ACTIVE':
      act_recs_ct += 1
    elif status == 'INACTIVE':
      inact_recs_ct += 1
    else:
      incarc_recs_ct += 1

live_recs_ct = len(live_recs)
if total_recs_ct != live_recs_ct + dead_recs_ct:
  logr.error('%s %d != %d + %d','wrong record counts',total_recs_ct, live_recs_ct, dead_recs_ct)

pdf.section_title('Who Is Included in the Statistics')
live_text = '''
The database includes people who are active, inactive, incarcerated and deceased. The statistics in this report include only living people because they can be affected by the use of this database. The table below shows that only a small fraction of people are excluded. 
'''
pdf.add_text(live_text)

tbl = [['Status','fraction','count'],
      ['active',act_recs_ct/total_recs_ct,act_recs_ct],
      ['inactive',inact_recs_ct/total_recs_ct,inact_recs_ct],
      ['incarcerated',incarc_recs_ct/total_recs_ct,incarc_recs_ct],
      ['all the above',live_recs_ct/total_recs_ct,live_recs_ct],
      ['deceased',dead_recs_ct/total_recs_ct,dead_recs_ct],
      ['total',total_recs_ct/total_recs_ct,total_recs_ct]]
pdf.basic_table('Person Status',tbl)
#}}}
#{{{ analyze gang member label
##################### analyzing the gang associate label ###################
primary_pts = []
missing_pri_ct = 0
for rec in live_recs:
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang['gang'] == 'PRIMARY':
        pts,cats = get_gang_crits(gang) 
        if pts != None:
          primary_pts.append(int(pts))
          break
        else:
          missing_pri_ct += 1
      else:
        missing_pri_ct += 1
  else:
    missing_pri_ct += 1

pdf.section_title('The Gang Member Label is Meaningless')

score_text = '''
The threshold for being labeled a "Gang Member" (10 pts) is also the highest frequency score in the database. It is doubtful that a person with a score of exactly 10 is any more or less likely to be a gang member than a person scoring 9 or 11. Seeing this label without the accompanying facesheet is misleading. 

It is even more problematic that over 30% of the scores are exactly 10 pt scores if BRIC stops updating records at that score. This makes reading the whole facesheet useless because it may be obsolete.
'''
pdf.add_text(score_text)


primary_pts_ct = len(primary_pts)
primary_pts_lt_6_ct = len([x for x in primary_pts if x < 6])
primary_pts_6_9_ct = len([x for x in primary_pts if 6 <= x < 10])
primary_pts_10_ct = primary_pts.count(10)
primary_pts_11_20_ct = len([x for x in primary_pts if 11 <= x < 21])
primary_pts_gt_20_ct = len([x for x in primary_pts if x > 20])
max_score = max(primary_pts)

if live_recs_ct != primary_pts_ct + missing_pri_ct:
  logr.error('%s %d != %d + %d','missing scores',live_recs_ct, primary_pts_ct,missing_pri_ct)

tbl = [['Score','fraction of scores','number of scores'],
      ['less than 6',primary_pts_lt_6_ct/primary_pts_ct,primary_pts_lt_6_ct],
      ['6 thru 9',primary_pts_6_9_ct/primary_pts_ct,primary_pts_6_9_ct],
      ['exactly 10',primary_pts_10_ct/primary_pts_ct,primary_pts_10_ct],
      ['11 thru 20',primary_pts_11_20_ct/primary_pts_ct,primary_pts_11_20_ct],
      ['greater than 20',primary_pts_gt_20_ct/primary_pts_ct,primary_pts_gt_20_ct]]

pdf.basic_table('Number of People with Each Score',tbl)

pts_max = 41
pts_scale = np.arange(pts_max)
pri_pts_hist = []
for i in pts_scale:
  pri_pts_hist.append(primary_pts.count(i))

total_scores = sum(pri_pts_hist)
pri_norm = [100*float(i)/total_scores for i in pri_pts_hist]

score_hist_png = 'score_hist.png'
score_plt = {'title':'Distribution of Primary Gang Scores',
            'xlabel':'Gang Scores',
            'ylabel':'Percent of Scores',
            'file_nm':score_hist_png}
one_bar_plot(pts_scale,pri_norm,score_plt)
#pdf.add_image(score_hist_png)
#pdf.add_note('The highest score recorded is ' + str(max_score) + '. The very small number of scores above 40 were omitted to make the graph more readable.')
#}}}
#{{{ FIO and BPD Report Analysis
##################### analyzing FIO and BPD Incident Reports ###################
fio_bpd_scores = []
for rec in live_recs:
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang['gang'] == 'PRIMARY':
        pts,cats = get_gang_crits(gang) 
        if pts != None and cats != None:
          rec_info = [pts,0,0] #pts, fios, bpds
          if 'contact_gang' in cats.keys(): 
            rec_info[1] = cats['contact_gang']
          if 'bpd_rpt' in cats.keys(): 
            rec_info[2] = cats['bpd_rpt']
          fio_bpd_scores.append(rec_info)

fio_bpd_frac = []
fio_bpd_once = []
fio_only_ct = 0
bpd_only_ct = 0
fio_bpd_only_ct = 0
other_pts_ct = 0
for dat in fio_bpd_scores:
  fio_pts = score_cats['contact_gang'][1]*dat[1]
  bpd_pts = score_cats['bpd_rpt'][1]*dat[2]
  fio_bpd_frac.append((fio_pts + bpd_pts)/dat[0])

  fio_bpd_adj_pts = dat[0]
  if dat[1] > 1:
    fio_bpd_adj_pts -= fio_pts - score_cats['contact_gang'][1]
  if dat[2] > 1:
    fio_bpd_adj_pts -= bpd_pts - score_cats['bpd_rpt'][1]
  fio_bpd_once.append(fio_bpd_adj_pts)

  if dat[0] == fio_pts:
    fio_only_ct += 1
  elif dat[0] == bpd_pts:
    bpd_only_ct += 1
  elif dat[0] == fio_pts + bpd_pts:
    fio_bpd_only_ct += 1
  else:
    other_pts_ct += 1

fio_bpd_frac_ct = len(fio_bpd_frac)
fio_bpd_frac_lt_20 = len([x for x in fio_bpd_frac if x < 0.2])
fio_bpd_frac_lt_40 = len([x for x in fio_bpd_frac if 0.2 <= x < 0.4])
fio_bpd_frac_lt_60 = len([x for x in fio_bpd_frac if 0.4 <= x < 0.6])
fio_bpd_frac_lt_80 = len([x for x in fio_bpd_frac if 0.6 <= x < 0.8])
fio_bpd_frac_ge_80 = len([x for x in fio_bpd_frac if x >= 0.8])

tbl = [['fios/bpds pts. per score','fraction of scores','number of scores'],
      ['0.8 up thru 1.0',fio_bpd_frac_ge_80/fio_bpd_frac_ct,fio_bpd_frac_ge_80],
      ['0.6 up to 0.8',fio_bpd_frac_lt_80/fio_bpd_frac_ct,fio_bpd_frac_lt_80],
      ['0.4 up to 0.6',fio_bpd_frac_lt_60/fio_bpd_frac_ct,fio_bpd_frac_lt_60],
      ['0.2 up to 0.4',fio_bpd_frac_lt_40/fio_bpd_frac_ct,fio_bpd_frac_lt_40],
      ['less than 0.2',fio_bpd_frac_lt_20/fio_bpd_frac_ct,fio_bpd_frac_lt_20]]

pdf.section_title('Gang Membership is Mostly Determined by Legal Activities')

score_text = '''
All the actvities in FIOs and BPD 1.1 Reports are completely legal as shown in these descriptions from BPD Rule 335. A person might not even know that the other party is a gang member.

CONTACT WITH KNOWN GANG MEMBERS/ASSOCIATES (FIO)
  Visiting, corresponding, or engaging in financial transactions with gang members or associated.
  2 points per interaction or transaction

DOCUMENTED ASSOCIATION (BPD 1.1/Incident Report)
  Walking, eating, recreating, communicating, or otherwise associating with confirmed gang members or associates.
  If not in custody or incarcerated: 4 points per interaction or transaction
  If in custody or incarcerated: 4 points per interaction or transaction

The table below shows how much of each score is composed of these two categories. The first row of the table below shows that over half the scores are getting 80 to 100% of their points from FIOs and BPD Reports.
'''
pdf.add_text(score_text)

pdf.basic_table('Fraction of Score that are FIOs and BPD Reports',tbl)

fio_bpd_ct = fio_only_ct + bpd_only_ct + fio_bpd_only_ct + other_pts_ct
no_fio_bpd_ct = live_recs_ct - fio_bpd_ct 
if fio_bpd_ct != len(fio_bpd_scores):
  logr.error('%s %d != %d ','missing fio_bpd scores',len(fio_bpd_scores), fio_bpt_ct)

text = '''
FIOs and BPD 1.1 Reports are the only categories in almost half of the scores in the database
'''
pdf.add_text(text)

tbl = [['categories','fraction','count'],
      ['fio only',fio_only_ct/live_recs_ct,fio_only_ct],
      ['bpd only',bpd_only_ct/live_recs_ct,bpd_only_ct],
      ['fio and bpd only',fio_bpd_only_ct/live_recs_ct,fio_bpd_only_ct],
      ['fio,bpd and others',other_pts_ct/live_recs_ct,other_pts_ct],
      ['no fios or bpds',no_fio_bpd_ct/live_recs_ct,no_fio_bpd_ct],
      ['total scores','1.0',live_recs_ct]]

pdf.basic_table('Number of Scores with FIOs and BPD 1.1 Reports',tbl)
pdf.add_note('The total number of scores is less then the number of active records because some records did not have valid scores')

fio_bpd_text = '''
Each BPD 1.1 Report or FIO adds points to a person's gang score. All other categories are counted just once The table below counts FIOs and BPD Reports only once. Comparing it to the table in Section 2 shows that the number of people labeled as gang members would drop from 98% to 39%.
'''
pdf.add_text(fio_bpd_text)

fio_bpd_once_hist = []
for i in pts_scale:
  fio_bpd_once_hist.append(fio_bpd_once.count(i))

total_scores = sum(fio_bpd_once_hist)
fio_bpd_once_norm = [100*float(i)/total_scores for i in fio_bpd_once_hist]

fio_bpd_hist_png = 'fio_bpd_hist.png'
score_plt = {'title':'Distribution of Primary Gang Scores',
            'xlabel':'Gang Scores',
            'ylabel':'Percent of Scores',
            'y1legend':'Actual Scores',
            'y2legend':'One FIO/BPD Report Scores',
            'file_nm':fio_bpd_hist_png}
#two_bar_plot(pts_scale,pri_norm,fio_bpd_once_norm,score_plt)
#pdf.add_image(fio_bpd_hist_png)


fio_bpd_ct = len(fio_bpd_once)
fio_bpd_once_lt_6_ct = len([x for x in fio_bpd_once if x < 6])
fio_bpd_once_6_9_ct = len([x for x in fio_bpd_once if 6 <= x < 10])
fio_bpd_once_10_ct = fio_bpd_once.count(10)
fio_bpd_once_11_20_ct = len([x for x in fio_bpd_once if 11 <= x < 21])
fio_bpd_once_gt_20_ct = len([x for x in fio_bpd_once if x > 20])
max_score = max(fio_bpd_once)


tbl = [['Score','fraction of scores','number of scores'],
      ['less than 6',fio_bpd_once_lt_6_ct/fio_bpd_ct,fio_bpd_once_lt_6_ct],
      ['6 thru 9',fio_bpd_once_6_9_ct/fio_bpd_ct,fio_bpd_once_6_9_ct],
      ['exactly 10',fio_bpd_once_10_ct/fio_bpd_ct,fio_bpd_once_10_ct],
      ['11 thru 20',fio_bpd_once_11_20_ct/fio_bpd_ct,fio_bpd_once_11_20_ct],
      ['greater than 20',fio_bpd_once_gt_20_ct/fio_bpd_ct,fio_bpd_once_gt_20_ct]]

pdf.basic_table('Number of People with Each Score (FIOs and BPD Reports just once)',tbl)
#}}}
#{{{ victim/target analysis
########################## victim/target analysis ##########################
victim_scores = []
for rec in live_recs:
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang['gang'] == 'PRIMARY':
        pts,cats = get_gang_crits(gang) 
        if pts != None and cats != None:
          rec_info = [pts,0,0] #pts, no_cust, cust
          if 'rival_grp_no_cust' in cats.keys(): 
            rec_info[1] = cats['rival_grp_no_cust']
          if 'rival_grp_cust' in cats.keys(): 
            rec_info[2] = cats['rival_grp_cust']
          if rec_info[1] != 0 or rec_info[2] != 0:
            victim_scores.append(rec_info)

victim_once = []
victim_none = []
for dat in victim_scores:
  no_cust_pts = score_cats['rival_grp_no_cust'][1]*dat[1]
  cust_pts = score_cats['rival_grp_cust'][1]*dat[2]
  victim_once.append(dat[0])

  victim_adj_pts = dat[0]
  if dat[1] > 0:
    victim_adj_pts -= score_cats['rival_grp_no_cust'][1]
  if dat[2] > 0:
    victim_adj_pts -= score_cats['rival_grp_cust'][1]
  victim_none.append(victim_adj_pts)

victim_once_ct = len(victim_once)
victim_once_lt_6_ct = len([x for x in victim_once if x < 6])
victim_once_6_9_ct = len([x for x in victim_once if 6 <= x < 10])
victim_once_10_ct = victim_once.count(10)
victim_once_11_20_ct = len([x for x in victim_once if 11 <= x < 21])
victim_once_gt_20_ct = len([x for x in victim_once if x > 20])

victim_none_ct = len(victim_none)
victim_none_lt_6_ct = len([x for x in victim_none if x < 6])
victim_none_6_9_ct = len([x for x in victim_none if 6 <= x < 10])
victim_none_10_ct = victim_none.count(10)
victim_none_11_20_ct = len([x for x in victim_none if 11 <= x < 21])
victim_none_gt_20_ct = len([x for x in victim_none if x > 20])

tbl = [['Score','with victim cat.','no victim cat.'],
      ['less than 6',victim_once_lt_6_ct,victim_none_lt_6_ct],
      ['6 thru 9',victim_once_6_9_ct,victim_none_6_9_ct],
      ['exactly 10',victim_once_10_ct,victim_none_10_ct],
      ['11 thru 20',victim_once_11_20_ct,victim_none_11_20_ct],
      ['greater than 20',victim_once_gt_20_ct,victim_none_gt_20_ct],
      ['total',victim_once_ct,victim_none_ct]]



pdf.section_title('Victim/Target of Rival Gang Category is Incomprehensible')
victim_text = '''
The description from BPD Rule 335 below mixes the victim and the perpetrator of a gang related threat or assault. It is unclear why a person involved should get a higher score if they are NOT in custody or incarcerated.

VICTIM / TARGET AFFILIATED WITH/MEMBER OF RIVAL GROUP
  An individual participated in a gang related threat or assault, or an individual has been the victim or target of rival gang members.
  If not in custody or incarcerated: 8 points
  If in custody or incarcerated: 3 points

 It sounds like a random person who gets mugged on the street by a gang member could get into this database with 80% of the points needed to be a gang member. The table below shows that victim/target gang membership would drop by about 45% if this category was removed.
 '''
pdf.add_text(victim_text)
pdf.basic_table('Number of Victims/Targets with Each Score',tbl)
#}}}
#{{{ category point distribution
##################### category points distribution #############################
cat_pts = {}
for key in score_cats.keys():
  cat_pts[key] = 0
#  crit_nms.append(key)

for rec in live_recs:
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang['gang'] == 'PRIMARY':
        pts,cats = get_gang_crits(gang) 
        if cats != None:
          for key in cats:
            cat_pts[key] += score_cats[key][1]*cats[key]

total_pts = 0
cats_pts_hist = []
for cat,pts in cat_pts.items():
  total_pts += pts
  cats_pts_hist.append([cat,pts])

cats_pts_hist = sorted(cats_pts_hist, key=lambda x: x[1],reverse=True)

tbl = [['catagory','pts per cat.','all cat. pts','fraction of total']]  
for cat in cats_pts_hist:
  cat_info = score_cats[cat[0]]
  #tbl.append([cat_info[3],cat_info[1],cat[1],cat[1]/total_pts])
  tbl.append([cat[0],cat_info[1],cat[1],cat[1]/total_pts])
tbl.append(['total database pts','',total_pts,'1.00'])

pdf.section_title('BRIC is Adding Little New Information')
cat_text = '''
FIOs and BPD 1.1 Reports account for 70% of the points in the database and the police already have those. Most of the other categories contribute 1% or less of the total points. It is not clear that this database helps the police prevent gang violence.
'''
pdf.add_text(cat_text)
pdf.basic_table('Total Database Points per Category',tbl)
#}}}
#{{{ address count correlation
adr_cts = []
scores = []
rec_most_mvs = None
rec_most_adrs = None
for idx,rec in enumerate(live_recs):
  rec_id = rec['pdf'] + '_' + str(rec['pg'])
  adr_ct = rec.get('adr_ct')
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang.get('gang') == 'PRIMARY':
        score = gang.get('pts')
        if adr_ct != None and score != None:
          rec_beg = rec.get('create')
          rec_fin = rec.get('update')
          if adr_ct != 0 and rec_beg != None and rec_fin != None:
            adr_cts.append(int(adr_ct))
            scores.append(int(score))
            tmp = per_wks(rec_beg,rec_fin)
            tmp2 = tmp/adr_ct
            if rec_most_mvs == None:
              rec_most_mvs = [idx,tmp2,adr_ct]
            if tmp2 < rec_most_mvs[1]:
              rec_most_mvs = [idx,tmp2,adr_ct]
      
          if rec_most_adrs == None:
            rec_most_adrs = [idx,adr_ct]
          if adr_ct > rec_most_adrs[1]:
            rec_most_adrs = [idx,adr_ct]


rec_most_adr_ct = rec_most_adrs[1]
rec_most = live_recs[rec_most_adrs[0]]
rec_most_id = rec_most['pdf'] + '_' + str(rec_most['pg'])
rec_most_age = per_wks(rec_most['create'],rec_most['update'])/52

rec_mvs = live_recs[rec_most_mvs[0]]
rec_mvs_id = rec_mvs['pdf'] + '_' + str(rec_mvs['pg'])
rec_mvs_age = per_wks(rec_mvs['create'],rec_mvs['update'])*7
rec_mvs_ct = rec_most_mvs[2]



xy_raw = list(zip(adr_cts,scores))
#xy_xclip = [x for x in xy_raw if x[0] < 200]
#xy_clip = [x for x in xy_xclip if x[1] < 100]
xy_xclip = [x for x in xy_raw if x[0] < 400]
xy_clip = [x for x in xy_xclip if x[1] < 800]
xy_sort = sorted(xy_clip, key=lambda x: x[0])
xy = list(zip(*xy_sort))
r = np.corrcoef(xy[0], xy[1])
corr_coeff = r[0][1]
a, b = np.polyfit(xy[0],xy[1],1)
x0 = xy[0][0]
x1 = xy[0][-1]
y0 = a*x0 + b
y1 = a*x1 + b
#mprint(r,a,b)


adrs_pts_png = 'adrs_pts.png'
adrs_pts_plt = {'title':'Address Counts vs Primary Gang Scores',
            'ylabel':'Address Count',
            'xlabel':'Gang Scores',
            #'line': [x0,x1,y0,y1],
            #'line': line,
            #'line': [a,b],
            'file_nm':adrs_pts_png}
#scatter_plot(xy[0],xy[1],adrs_pts_plt)
scatter_plot(xy[1],xy[0],adrs_pts_plt)

pdf.section_title('Do the Addresses in A Facesheet Mean Anything?')
victim_text = f'''
 BPD Rule 335 does not explain what the address section of a facesheet means or how it was collected. The entries are so heavily redacted that counting the number of addresses on each facesheet seems to be the mostly likely way to deduce some meaning.

The facesheet with the most addresses has facesheet ID {rec_most_id} with {rec_most_adr_ct}. It is highly unlikely that anyone has this many confirmed residential addresses in the {rec_most_age:.1f} years that they have been in this database.

The person at facesheet ID {rec_mvs_id} has accumulated {rec_mvs_ct} in {rec_mvs_age:.1f} days. Obviously there were not this many sightings of this person in one day. Could these addresses be cell phone call records obtained from the phone companies? Is that legal without a search warrant?
 '''
pdf.add_text(victim_text)
pdf.add_note('The facesheet IDs above tell you where to find these records in the gang database pdfs. So "3501_277" points to page 277 in 3501-4000-Redacted.pdf.') 

relation_text = f'''
Finally the correlation coefficient between the number of addresses in a facesheet and its gang membership score is {corr_coeff:.2f}. A coefficient of 0.00 indicates complete randomness. This can be seen from the scatter plot of the same data below. In the top left corner is person with the most addresses and only 20 points on the gang database score. And all along the bottom of the plot are scores 3 times as high with less than 50 addresses. The majority of facesheets are packed randomly into the lower left corner of the plot.

It would be good to know what the BPD thinks these addresses mean.
'''
pdf.add_text(relation_text)
pdf.add_image(adrs_pts_png)
#}}}
#{{{ Report Details Analysis
flags_hist = {}
for key in flag_wds.keys():
  flags_hist[key] = 0
flags_hist['none'] = 0

flagged_pts = 0
flagged_recs_ct = 0
flagged_recs = []
unflagged_recs = []
violent_recs = []
nonviolent_recs = []
for rec in live_recs:
  flags = rec.get('flags')
  gangs = rec.get('gangs')
  if gangs != None:
    for gang in gangs:
      if gang['gang'] == 'PRIMARY':
        pts = int(gang.get('pts'))

  if len(flags) > 0:
    violence_flag = False
    for key in flags:
      if key in violent_flags:
        violence_flag = True

    for key in flags_hist.keys():
      if key in flags:
        flags_hist[key] += 1

      if pts != None:
        flagged_pts += pts
        flagged_recs_ct += 1
        flagged_recs.append(pts)


    if violence_flag == True:
      violent_recs.append(pts)
    else:
      nonviolent_recs.append(pts)



  else:
    flags_hist['none'] += 1
    if pts != None:
      unflagged_recs.append(pts)
     

flagged_recs_avg_pts = flagged_pts/flagged_recs_ct
unflagged_recs_avg_pts = (total_pts - flagged_pts)/(live_recs_ct - flagged_recs_ct)

unflagged_med = int(statistics.median(unflagged_recs))
flagged_med = int(statistics.median(flagged_recs))
nonviolent_med = int(statistics.median(nonviolent_recs))
violent_med = int(statistics.median(violent_recs))
#print(flagged_med,unflagged_med,violent_med,nonviolent_med)
max_score = max(primary_pts)



tbl = [['category','reports per cat.']]  
for cat in flags_hist:
  #tbl.append([cat_info[3],cat_info[1],cat[1],cat[1]/total_pts])
  tbl.append([cat,flags_hist[cat]])
tbl.append(['total reports',live_recs_ct])

no_flags_frac = flags_hist['none']/live_recs_ct

pdf.section_title('Report Details Keyword Analysis')
keyword_text = f'''
The Verification Report Details section at the end of each facesheet is heavily redacted but may contain keywords that indicate criminal or suspicious activity. Those keywords are divided into the following categories that can be flagged in the facesheets. An explanation of these flagged categories and the keywords for them are in the appendix at the end of this report.

The table below shows the categories and how many facesheets contain the keywords for each category. The first thing to notice is that the majority of facesheets ({no_flags_frac:.2f}) contain none of the analysis keywords.

 '''
pdf.add_text(keyword_text)
pdf.basic_table('Total Records per Category',tbl)

violence_text = f'''
The keywords in the Verification Details have a weak correlation with the gang assessment points. The median score for all the records that have at least one of these keywords is {flagged_med} and the median score for those that have none is {unflagged_med}.

The first five categories in the table above (homicide,guns,weapon,violence,threats) seem to have an even stronger correlationwith the gang score. The median score for all the records that have at least one of the "violence" categories is {violent_med} and the median score for those that have only the other categories is {nonviolent_med}. These other categories (drugs'arrest,robbery,damage,online) have the same median as the records with no category words at all.

These five "violence" categories and their keywords are the only information in this database that seem to have any correlation with the gang assessment scores. It would be interesting to know if these Verification Details sections are what the police actually look at to assess who is likely to engage in violence.
'''
pdf.add_text(violence_text)
pdf.add_note('Median scores are used rather than means because there are several very high outlying scores that would skew the mean.') 
#}}}
#{{{ final thoughts
pdf.page_break()
pdf.section_title('A Final Thought')
final_text = '''
In the Greater Boston Debate Series debate on June 29, former BPD commissioner Ed Davis said gang violence has decreased since the database was created. He was implying causality that he didn't prove and I assume advocates of the database will use this argument again. It should be challenged, otherwise the discussion becomes about weighing demonstrated harm to real people against an unsupported claim about benefits to the community. I hope this data helps make that challenge. 
'''
pdf.add_text(final_text)
#}}}
#{{{ Category Keyword Appendix
pdf.section_title('Appendix - Verification Details Category Keywords')
keyword_text = f'''
The table below shows each category and its keywords in the Verification Details section of a facesheet. This list was created manually from a list of all the words in all the facesheets so some words that would naturally seem to belong here are omitted because they never occur in the database.
'''
pdf.add_text(keyword_text)
tbl = [['category','keywords']]
for key,wds in flag_wds.items():
  tbl.append([key,','.join(wds)])
pdf.basic_table('Category Keywords',tbl)
#}}}

pdf.output(args.outf)

