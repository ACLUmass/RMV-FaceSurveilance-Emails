#!/usr/bin/python3
#https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
from tkinter import *

from tkinter import messagebox

class view():
  def __init__(self): #setup everything without controller callbacks
    self.top = Tk()
    self.top.geometry("100x100")

  def setCtlBacks(self,callback): #setup the stuff with controller callbacks 
    self.B = Button(self.top, text = "Hello", command = callback)
    self.B.place(x = 50,y = 50)

#view part of all callbacks go here
  def helloCallBack(self,title,words):
    self.msg = messagebox.showinfo(title,words)
#all other stuff
  def buttonChg(self,msg):
    self.B.config(text = msg)

  def run(self):
    self.top.mainloop()

