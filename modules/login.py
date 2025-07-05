from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Login")
root.geometry("800x400+200+100")
root.configure(bg="#fff")
root.resizable(False, False)

#setting logo
image = PhotoImage(file="assets/login.png") #path gambar logo
Label(root, image=image, bg="white").place(x=50, y=10)

#setting form login
frame = Frame(root, width=300, height=300, bg="red")
frame.place(x=450, y=50)

root.mainloop()