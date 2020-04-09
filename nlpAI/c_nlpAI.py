#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

import view

#create the view object first because it will be needed in callbacks
v = view.view()

#create all the controller methods that the view object uses as callbacks
def helloCallBack():
  #put controller part of callback response here.......
  v.helloCallBack( "Hello Python", "Hello World") #view part of callback is here
  v.buttonChg('bye')

v.setCtlBacks(helloCallBack) #give view pointers to controller callback methods
v.run() #run the tkinter loop
