from tkinter import *
from tkinter import messagebox
from modules.database import get_db_connection, hash_password

# Fungsi untuk kembali ke halaman login (menggunakan jendela utama yang sama)
def show_login_page(current_window):
    # *** PENTING: Import LoginApp di dalam fungsi ini (relatif) ***
    from .login import LoginApp # <--- PERUBAHAN DI SINI (TITIK DEPANNYA)
    LoginApp(current_window) 

def RegisterApp(register_window):
    # register_window adalah jendela Tk() utama yang sama dari main.py
    # Bersihkan semua widget lama dari jendela jika ada
    for widget in register_window.winfo_children():
        widget.destroy()

    register_window.title("Register")
    register_window.geometry("800x450+200+100")
    register_window.configure(bg="#fff")
    register_window.resizable(False, False)

    def register_action():
        email = user_entry.get()
        username = username_entry.get() 
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if email == "" or username == "" or password == "" or confirm_password == "" or \
           email == "Email" or username == "Username" or password == "Password" or confirm_password == "Confirm Password":
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return
        
        if not "@" in email or not "." in email:
            messagebox.showerror("Error", "Format email tidak valid!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Password tidak cocok!")
            return

        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, username, password, level) VALUES (?, ?, ?, ?)",
                           (email, username, hashed_password, "siswa")) 
            conn.commit()
            messagebox.showinfo("Success", "Registrasi berhasil! Silakan login.")
            show_login_page(register_window) # Kembali ke halaman login setelah registrasi berhasil
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "Email sudah terdaftar. Gunakan email lain.")
            else:
                messagebox.showerror("Error", f"Terjadi kesalahan saat registrasi: {e}")
        finally:
            conn.close()

    image = PhotoImage(file="assets/logo2.png")  
    image = image.subsample(2, 2)  
    Label(register_window, image=image, border=0, bg="white").place(x=90, y=50)
    register_window.image_reference_register = image 

    frame = Frame(register_window, width=300, height=400, bg="#fff")
    frame.place(x=450, y=50)

    heading = Label(frame, text="Register", fg="#57a1f8", font=("Microsoft YaHei UI Light", 23, "bold"), bg="white")
    heading.place(x=100, y=5)

    ##########-----------------------------------
    def on_enter_user(e):
        if user_entry.get() == 'Email':
            user_entry.delete(0, 'end')
    def on_leave_user(e):
        if user_entry.get() == '':
            user_entry.insert(0, "Email")

    user_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    user_entry.place(x=25, y=70)
    user_entry.insert(0, "Email")
    user_entry.bind("<FocusIn>", on_enter_user)
    user_entry.bind("<FocusOut>", on_leave_user)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=100)

    ##########-----------------------------------
    def on_enter_username(e):
        if username_entry.get() == 'Username':
            username_entry.delete(0, 'end')
    def on_leave_username(e):
        if username_entry.get() == '':
            username_entry.insert(0, "Username")

    username_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    username_entry.place(x=25, y=120)
    username_entry.insert(0, "Username")
    username_entry.bind("<FocusIn>", on_enter_username)
    username_entry.bind("<FocusOut>", on_leave_username)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=150)

    ##########-----------------------------------
    def on_enter_code(e):
        if password_entry.get() == 'Password':
            password_entry.delete(0, 'end')
            password_entry.config(show="*")
    def on_leave_code(e):
        if password_entry.get() == '':
            password_entry.insert(0, "Password")
            password_entry.config(show="")

    password_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    password_entry.place(x=25, y=170)
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", on_enter_code)
    password_entry.bind("<FocusOut>", on_leave_code)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=200)

    ##########-----------------------------------
    def on_enter_confirm_code(e):
        if confirm_password_entry.get() == 'Confirm Password':
            confirm_password_entry.delete(0, 'end')
            confirm_password_entry.config(show="*")
    def on_leave_confirm_code(e):
        if confirm_password_entry.get() == '':
            confirm_password_entry.insert(0, "Confirm Password")
            confirm_password_entry.config(show="")

    confirm_password_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    confirm_password_entry.place(x=25, y=220)
    confirm_password_entry.insert(0, "Confirm Password")
    confirm_password_entry.bind("<FocusIn>", on_enter_confirm_code)
    confirm_password_entry.bind("<FocusOut>", on_leave_confirm_code)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=250)

    ############------------------------------------
    Button(frame, width=39, pady=7, text="Register", bg="#57a1f8", fg="white", border=0, command=register_action).place(x=25, y=270)
    label = Label(frame, text="Already have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
    label.place(x=65, y=330)

    login_btn = Button(frame, width=6, text="Login", border=0, bg="white", fg="#57a1f8", cursor="hand2", command=lambda: show_login_page(register_window))
    login_btn.place(x=210, y=330)

# Blok ini hanya untuk pengujian jika register.py dijalankan langsung
if __name__ == '__main__':
    window_test = Tk()
    RegisterApp(window_test)
    window_test.mainloop()