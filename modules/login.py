# modules/login.py

from tkinter import *
from tkinter import messagebox
from modules.database import get_db_connection, check_password

# Fungsi untuk membuka jendela dashboard siswa/admin
# Menerima root_window dan juga username
def open_dashboard(user_level, root_window, username): # <--- TAMBAHKAN 'username' DI SINI
    root_window.withdraw() # Sembunyikan jendela root (login/register)
    
    if user_level == "siswa":
        from modules.dashboard_siswa import open_siswa_dashboard
        open_siswa_dashboard(root_window, username) # <--- TERUSKAN 'username' KE SINI
    elif user_level == "admin":
        from modules.dashboard_admin import open_admin_dashboard
        open_admin_dashboard(root_window, username) # Teruskan 'username' untuk dashboard admin juga (akan kita sesuaikan nanti)

# Fungsi yang akan dipanggil oleh main.py atau register.py untuk inisialisasi aplikasi login
def LoginApp(root_window):
    # Bersihkan semua widget lama dari jendela jika ada
    for widget in root_window.winfo_children():
        widget.destroy()

    root_window.title("Login")
    root_window.geometry("800x400+200+100")
    root_window.configure(bg="#fff")
    root_window.resizable(False, False)

    def login_action():
        email = user_entry.get()
        password = password_entry.get()

        if email == "Email" or password == "Password" or not email or not password:
            messagebox.showerror("Login Error", "Mohon isi semua kolom!")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            if check_password(user_data['password'], password):
                messagebox.showinfo("Login Success", f"Selamat datang, {user_data['username']}!")
                # Panggil open_dashboard dengan user_data['username']
                open_dashboard(user_data['level'], root_window, user_data['username']) # <--- TERUSKAN user_data['username']
            else:
                messagebox.showerror("Login Error", "Password salah!")
        else:
            messagebox.showerror("Login Error", "Email tidak ditemukan!")

    # Fungsi untuk berpindah ke halaman register
    def show_register_page():
        # Import RegisterApp di dalam fungsi ini untuk menghindari circular import
        from .register import RegisterApp 
        RegisterApp(root_window) 

    # setting logo
    try:
        image = PhotoImage(file="assets/logo.png") 
        image = image.subsample(2, 2)
        Label(root_window, image=image, bg="white").place(x=90, y=50)
        root_window.image_reference_login = image # Simpan referensi gambar
    except Exception as e:
        print(f"Error loading assets/logo.png: {e}")
        Label(root_window, text="Logo", font=("Arial", 20), bg="white").place(x=90, y=50)

    # setting form login
    frame = Frame(root_window, width=300, height=300, bg="white")
    frame.place(x=450, y=50)

    heading = Label(frame, text="Login", fg="#57a1f8", font=("Microsoft YaHei UI Light", 23, "bold"), bg="white")
    heading.place(x=100, y=5)

    ########-----------------------------------
    def on_enter_user(e):
        if user_entry.get() == "Email":
            user_entry.delete(0, 'end')
        
    def on_leave_user(e):
        name = user_entry.get()
        if name == '':
            user_entry.insert(0, "Email")

    user_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    user_entry.place(x=25, y=70)
    user_entry.insert(0, "Email")
    user_entry.bind("<FocusIn>", on_enter_user)
    user_entry.bind("<FocusOut>", on_leave_user)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=100)

    ########-----------------------------------
    def on_enter_code(e):
        if password_entry.get() == "Password":
            password_entry.delete(0, 'end')
            password_entry.config(show="*")
        
    def on_leave_code(e):
        name = password_entry.get()
        if name == '':
            password_entry.insert(0, "Password")
            password_entry.config(show="")

    password_entry = Entry(frame, width=25, fg="black", font=("Microsoft YaHei UI Light", 11), bg="white", border=0)
    password_entry.place(x=25, y=140)
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", on_enter_code)
    password_entry.bind("<FocusOut>", on_leave_code)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=170)

    ########################################################
    Button(frame, width=39, pady=7, text="Login", bg="#57a1f8", fg="white", border=0, command=login_action).place(x=25, y=210)
    label = Label(frame, text="Don't have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
    label.place(x=75, y=270)

    register_btn = Button(frame, width=6, text="Register", border=0, bg="white", fg="#57a1f8", cursor="hand2", command=show_register_page)
    register_btn.place(x=210, y=270)

# Blok ini hanya untuk pengujian jika login.py dijalankan langsung
if __name__ == '__main__':
    root_test = Tk()
    LoginApp(root_test)
    root_test.mainloop()