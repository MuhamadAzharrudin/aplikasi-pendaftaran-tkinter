from tkinter import *
from tkinter import messagebox

# Pastikan fungsi ini menerima root_window
def open_siswa_dashboard(root_window): # <--- PERUBAHAN DI SINI
    dashboard_siswa_window = Toplevel(root_window) 
    dashboard_siswa_window.title("Dashboard Siswa")
    dashboard_siswa_window.geometry("800x400+200+100")
    dashboard_siswa_window.configure(bg="#e6ffe6") 
    
    # Sembunyikan root_window saat dashboard terbuka
    root_window.withdraw()

    Label(dashboard_siswa_window, text="Selamat Datang, Siswa!", 
          font=("Helvetica", 24, "bold"), bg="#e6ffe6", fg="#336633").pack(pady=50)
    Label(dashboard_siswa_window, text="Ini adalah dashboard khusus untuk Siswa.", 
          font=("Arial", 14), bg="#e6ffe6", fg="#333333").pack(pady=10)

    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_siswa_window.destroy()
            # Munculkan kembali jendela utama (root_window) dan tampilkan login
            root_window.deiconify() 
            # Hapus semua widget lama di root_window sebelum mengisi dengan login
            for widget in root_window.winfo_children():
                widget.destroy()
            # *** PENTING: Import LoginApp di dalam fungsi logout ***
            from modules.login import LoginApp # <--- Perubahan path import
            LoginApp(root_window) 

    Button(dashboard_siswa_window, text="Logout", command=logout, 
           font=("Arial", 12), bg="#ff6666", fg="white", padx=10, pady=5).pack(pady=20)

    # Tambahkan protokol untuk menangani penutupan jendela dashboard
    def on_closing_dashboard():
        if messagebox.askyesno("Keluar", "Anda yakin ingin menutup dashboard?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            # *** PENTING: Import LoginApp di dalam fungsi on_closing_dashboard ***
            from modules.login import LoginApp # <--- Perubahan path import
            LoginApp(root_window)

    dashboard_siswa_window.protocol("WM_DELETE_WINDOW", on_closing_dashboard)

    if __name__ == '__main__':
        # Jika dashboard_siswa.py dijalankan langsung untuk pengujian, 
        # buat root_test dan panggil dengan itu
        root_test_direct = Tk()
        open_siswa_dashboard(root_test_direct)
        root_test_direct.mainloop()