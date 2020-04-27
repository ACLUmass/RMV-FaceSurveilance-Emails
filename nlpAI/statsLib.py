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

