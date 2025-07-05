from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Login")
root.geometry("800x400+200+100")
root.configure(bg="#fff")
root.resizable(False, False)

def register():
    email = user.get()
    password = code.get()
    if email == "admin" or password == "123":
        screen = Toplevel(root)
        screen.title("Welcome")
        screen.geometry("800x400+200+100")
        screen.config(bg="white")
        
        Label(screen, text="Hallo Semuanya", bg="white", font=("Microsoft YaHei UI Light", 50, "bold")).pack(expand=True)
        screen.mainloop()
    elif email != "admin" and password != "123":
        messagebox.showerror("Invalid", "Invalid Email or Password")

#setting logo
image = PhotoImage(file="assets/login.png") #path gambar logo
Label(root, image=image, bg="white").place(x=50, y=10)

#setting form login
frame = Frame(root, width=300, height=300, bg="white")
frame.place(x=450, y=50)

heading = Label(frame, text="Login", fg="#57a1f8", font=("Microsoft YaHei UI Light", 23, "bold"), bg="white")
heading.place(x=100, y=5)

########-----------------------------------
def on_enter(e):
    user.delete(0, 'end')
    
def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, "Email")

user = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
user.place(x=25, y=70)
user.insert(0, "Email")
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)


Frame(frame, width=295, height=2, bg="black").place(x=25, y=100)

########-----------------------------------
def on_enter(e):
    code.delete(0, 'end')
    
def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, "Password")

code = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
code.place(x=25, y=140)
code.insert(0, "Password")
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=170)

########################################################
Button(frame, width=39, pady=7, text="Login", bg="#57a1f8", fg="white", border=0, command=register).place(x=25, y=210)
label = Label(frame, text="Don't have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
label.place(x=75, y=270)

register = Button(frame, width=6, text="Register", border=0, bg="white", fg="#57a1f8", cursor="hand2")
register.place(x=210, y=270)


root.mainloop()