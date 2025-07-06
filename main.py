from tkinter import Tk
from modules.database import create_tables
from modules.login import LoginApp # <--- PERUBAHAN DI SINI

if __name__ == '__main__':
    # Inisialisasi database (buat tabel jika belum ada)
    create_tables()

    # Buat instance Tkinter utama
    root = Tk()
    # Panggil fungsi LoginApp dengan instance root
    LoginApp(root)
    # Jalankan loop utama Tkinter
    root.mainloop()