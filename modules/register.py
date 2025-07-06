from tkinter import *
from tkinter import messagebox
import ast

window = Tk()
window.title("Register")
window.geometry("800x400+200+100")
window.configure(bg="#fff")
window.resizable(False, False)

def register():
    email = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    if email == "" or password == "" or confirm_password == "":
        messagebox.showerror("Error", "All fields are required")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
    else:
        # Here you can add code to save the user data
        messagebox.showinfo("Success", "Registration successful")
        window.destroy()  # Close the registration window

image = PhotoImage(file="assets/logo2.png")  # Path to logo image
image = image.subsample(2, 2)  # megubah ukuran gambar jika diperlukan
Label(window, image=image, border=0, bg="white").place(x=90, y=50)

frame = Frame(window, width=300, height=400, bg="#fff")
frame.place(x=450, y=50)

heading = Label(frame, text="Register", fg="#57a1f8", font=("Microsoft YaHei UI Light", 23, "bold"), bg="white")
heading.place(x=100, y=5)

##########-----------------------------------
def on_enter(e):
    user.delete(0, 'end')
def on_leave(e):
    if user.get() == '':
        user.insert(0, "Email")

user = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
user.place(x=25, y=70)
user.insert(0, "Email")
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=100)

##########-----------------------------------
def on_enter(e):
    code.delete(0, 'end')
def on_leave(e):
    if code.get() == '':
        code.insert(0, "Password")

code = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
code.place(x=25, y=120)
code.insert(0, "Password")
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=150)

##########-----------------------------------
def on_enter(e):
    confirm_code.delete(0, 'end')
def on_leave(e):
    if confirm_code.get() == '':
        confirm_code.insert(0, "Confirm Password")

confirm_code = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
confirm_code.place(x=25, y=170)
confirm_code.insert(0, "Confirm Password")
confirm_code.bind("<FocusIn>", on_enter)
confirm_code.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=200)

############------------------------------------
Button(frame, width=39, pady=7, text="Register", bg="#57a1f8", fg="white", border=0, command=register).place(x=25, y=220)
label = Label(frame, text="Already have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
label.place(x=65, y=280)

login = Button(frame, width=6, text="Login", border=0, bg="white", fg="#57a1f8", cursor="hand2")
login.place(x=210, y=280)

window.mainloop()