from tkinter import *
from tkinter import messagebox
from modules.database import get_db_connection 

# Pastikan fungsi ini menerima root_window
def open_admin_dashboard(root_window): # <--- PERUBAHAN DI SINI
    dashboard_admin_window = Toplevel(root_window) 
    dashboard_admin_window.title("Dashboard Admin")
    dashboard_admin_window.geometry("1000x600+100+50")
    dashboard_admin_window.configure(bg="#ffe6e6") 

    # Sembunyikan root_window saat dashboard terbuka
    root_window.withdraw()

    Label(dashboard_admin_window, text="Selamat Datang, Admin!", 
          font=("Helvetica", 28, "bold"), bg="#ffe6e6", fg="#990000").pack(pady=30)
    Label(dashboard_admin_window, text="Ini adalah dashboard manajemen Admin.", 
          font=("Arial", 16), bg="#ffe6e6", fg="#660000").pack(pady=10)

    def show_users():
        for widget in dashboard_admin_window.winfo_children():
            if isinstance(widget, Frame) and "user_list_frame" in str(widget):
                widget.destroy()

        user_list_frame = Frame(dashboard_admin_window, bg="#ffffff", bd=2, relief="groove")
        user_list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        Label(user_list_frame, text="Daftar Pengguna:", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, username, level FROM users")
        users = cursor.fetchall()
        conn.close()

        if users:
            header_frame = Frame(user_list_frame, bg="#f0f0f0")
            header_frame.pack(fill="x", padx=10, pady=5)
            Label(header_frame, text="ID", font=("Arial", 10, "bold"), width=5, bg="#f0f0f0").pack(side=LEFT, padx=5)
            Label(header_frame, text="Email", font=("Arial", 10, "bold"), width=30, bg="#f0f0f0").pack(side=LEFT, padx=5)
            Label(header_frame, text="Username", font=("Arial", 10, "bold"), width=20, bg="#f0f0f0").pack(side=LEFT, padx=5)
            Label(header_frame, text="Level", font=("Arial", 10, "bold"), width=10, bg="#f0f0f0").pack(side=LEFT, padx=5)

            for user in users:
                user_row_frame = Frame(user_list_frame, bg="#ffffff")
                user_row_frame.pack(fill="x", padx=10)
                Label(user_row_frame, text=user['id'], width=5, bg="#ffffff").pack(side=LEFT, padx=5)
                Label(user_row_frame, text=user['email'], width=30, bg="#ffffff").pack(side=LEFT, padx=5)
                Label(user_row_frame, text=user['username'], width=20, bg="#ffffff").pack(side=LEFT, padx=5)
                Label(user_row_frame, text=user['level'], width=10, bg="#ffffff").pack(side=LEFT, padx=5)
        else:
            Label(user_list_frame, text="Tidak ada pengguna terdaftar.", bg="#ffffff").pack(pady=10)

    Button(dashboard_admin_window, text="Lihat Daftar Pengguna", command=show_users, 
           font=("Arial", 12), bg="#57a1f8", fg="white", padx=10, pady=5).pack(pady=10)

    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_admin_window.destroy()
            root_window.deiconify() 
            for widget in root_window.winfo_children():
                widget.destroy()
            # *** PENTING: Import LoginApp di dalam fungsi logout ***
            from modules.login import LoginApp # <--- Perubahan path import
            LoginApp(root_window) 

    Button(dashboard_admin_window, text="Logout", command=logout, 
           font=("Arial", 12), bg="#ff6666", fg="white", padx=10, pady=5).pack(pady=20)

    # Tambahkan protokol untuk menangani penutupan jendela dashboard
    def on_closing_dashboard():
        if messagebox.askyesno("Keluar", "Anda yakin ingin menutup dashboard?"):
            dashboard_admin_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            # *** PENTING: Import LoginApp di dalam fungsi on_closing_dashboard ***
            from modules.login import LoginApp # <--- Perubahan path import
            LoginApp(root_window)

    dashboard_admin_window.protocol("WM_DELETE_WINDOW", on_closing_dashboard)

    if __name__ == '__main__':
        # Jika dashboard_admin.py dijalankan langsung untuk pengujian
        root_test_direct = Tk()
        open_admin_dashboard(root_test_direct)
        root_test_direct.mainloop()