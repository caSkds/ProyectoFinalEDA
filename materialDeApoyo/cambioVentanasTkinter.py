import tkinter as tk

myApp = tk.Tk()


myFirstWindow = tk.Frame(myApp, width=300, height=200)
mySecondWindow = tk.Frame(myApp, width=300, height=200)

button1 = tk.Button(myFirstWindow, text="Open Second Window")

def openSecondWindow():
    myFirstWindow.pack_forget()
    mySecondWindow.pack()

button1.config(command=openSecondWindow)
button1.pack()

def openFirstWindow():
    mySecondWindow.pack_forget()
    myFirstWindow.pack()

button2 = tk.Button(mySecondWindow, text="Open First Window")
button2.config(command=openFirstWindow)
button2.pack()

myFirstWindow.pack()
myApp.mainloop()
