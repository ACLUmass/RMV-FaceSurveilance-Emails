#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

import sys
import v_nlpAI as view
import m_nlpAI as model

#create the view object first because it will be needed in callbacks
v = view.view()
hypo = "True "

m = model.model(sys.argv[1])

#create all the controller methods that the view object uses as callbacks
def hypoCback():
  global hypo  #NOTE - this belongs in model
  #put controller part of callback response here.......
  if hypo == "True ":
    hypo = "False"
  else:
    hypo = "True "
  v.hypoVback(hypo) #view part of callback is here

def nextCback():
  (mailId,email) = m.getMail()
  v.nextVback(mailId,email) #view part of callback is here

def prevCback():
  return

def modeCback():
  return

def gotoCback():
  return

def runAICback():
  return

v.hypoVback(hypo)
v.setVbacks(hypoCback,nextCback,prevCback,modeCback,gotoCback,runAICback) #give view pointers to controller callback methods
v.run() #run the tkinter loop
