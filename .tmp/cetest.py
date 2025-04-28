
# Import Required Library 
from tkinter import *
  
# Create Object 
root = Tk() 
  
# Set geometry 
root.geometry("400x400") 

def testCu():
    root.config(cursor="cross")

def testCu2():
    root.config(cursor="")

Button(root,text="Button",font=("Helvetica 15 bold"),command=testCu).pack()
Button(root,text="Button2",font=("Helvetica 15 bold"),command=testCu2).pack()

# Execute Tkinter 
root.mainloop()
