#!/usr/bin/python3
import math
import scipy.stats

#https://en.wikipedia.org/wiki/Margin_of_error
#https://www.statisticshowto.com/probability-and-statistics/find-sample-size/

def samSz(conf,ptrue,popSz): #confidence, expected true proportion, population size
  #conf = how confident we want to be that we didn't reject a True result
  #ptrue = expected proportion or result
  err =  0.05 #confidence is 0.9 +/- err
  zscore = scipy.stats.norm.ppf((1.0 + conf)/2.0) #z-score
  ssz = (zscore*zscore*ptrue*(1-ptrue))/(err*err) #cochran formula 
  return (ssz/(1.0 + (ssz - 1.0)/popSz)) #modified for small populatons

#https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa/20864883#20864883
def samConf(fSz,err,ptrue,popSz): #sample size, expected true proportion, population size
  #err = 0.05
  if popSz == fSz: #whole populaton was sampled
    return 1.0
  else:
    rSz = fSz*(popSz - 1.0)/(popSz - fSz) #modified for small populatons
  zscore = math.sqrt((rSz*err*err)/(ptrue*(1.0-ptrue))) #cochran formula 
  return(2.0*scipy.stats.norm.cdf(zscore)) - 1.0 #confidence

  

