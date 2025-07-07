# modules/dashboard_siswa.py

from tkinter import *
from tkinter import messagebox
import customtkinter

# Pastikan fungsi ini menerima root_window dan username
def open_siswa_dashboard(root_window, username):
    dashboard_siswa_window = Toplevel(root_window) 
    dashboard_siswa_window.title(f"Dashboard Siswa - {username}")
    dashboard_siswa_window.geometry("1000x600+100+50")
    dashboard_siswa_window.configure(bg="#f0f0f0") 
    dashboard_siswa_window.resizable(True, True)

    root_window.withdraw()

    main_frame = Frame(dashboard_siswa_window, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True)

    sidebar_frame = customtkinter.CTkFrame(main_frame, width=200, corner_radius=0, fg_color="#093FB4") 
    sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)
    sidebar_frame.pack_propagate(False) # Penting agar lebar sidebar tetap

    content_frame = Frame(main_frame, bg="#ffffff")
    content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # --- Logout Function ---
    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify() 
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp 
            LoginApp(root_window) 

    # --- Protocol untuk menangani penutupan jendela dashboard ---
    def on_closing_dashboard():
        if messagebox.askyesno("Keluar", "Anda yakin ingin menutup dashboard?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp 
            LoginApp(root_window)
            
    dashboard_siswa_window.protocol("WM_DELETE_WINDOW", on_closing_dashboard)


    # --- Sidebar Content ---
    welcome_label = customtkinter.CTkLabel(sidebar_frame, text=f"Selamat Datang,\n{username}!", 
                                  font=("Helvetica", 18, "bold"), text_color="white", fg_color="#093FB4",
                                  wraplength=180, justify="center")
    welcome_label.pack(pady=(20, 30), padx=10) # Padding bawah tetap untuk jarak dari tombol

    # HILANGKAN spacer_frame DI SINI
    # spacer_frame = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent")
    # spacer_frame.pack(fill="both", expand=True) 

    # --- Frame untuk Tombol-Tombol Menu Utama ---
    menu_buttons_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    # KEMBALIKAN expand=True di sini agar menu_buttons_container mengambil sisa ruang
    menu_buttons_container.pack(fill="both", expand=True) 

    # --- Frame untuk Tombol Logout ---
    logout_button_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    logout_button_container.pack(fill="x", pady=(10, 20))


    # Fungsi untuk menampilkan konten di content_frame (hanya konten yang relevan)
    def show_page(page_name):
        for widget in content_frame.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            title_label = customtkinter.CTkLabel(content_frame, text="SELAMAT DATANG CALON SISWA BARU!",
                                                font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)

            scrollable_dashboard_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="transparent")
            scrollable_dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            detail_pendaftaran_card = customtkinter.CTkFrame(scrollable_dashboard_frame, 
                                                            fg_color="white", corner_radius=10,
                                                            border_color="#093FB4", border_width=1)
            detail_pendaftaran_card.pack(fill="x", padx=10, pady=(10, 20))

            Label(detail_pendaftaran_card, text="Detail Pendaftaran Anda", 
                  font=("Helvetica", 16, "bold"), bg="white", fg="#333333").pack(padx=15, pady=(15, 5)) 
            
            dummy_data_pendaftaran = {
                "Nama Lengkap": f"Calon Siswa {username}",
                "Tempat, Tanggal Lahir": "Jakarta, 01 Januari 2008",
                "Asal Sekolah": "SMP Negeri 1 Jakarta",
                "Program Pilihan": "IPA",
                "Nomor HP": "0812-3456-7890",
                "Email": "calonsiswa@example.com"
            }
            
            for key, value in dummy_data_pendaftaran.items():
                row_frame = Frame(detail_pendaftaran_card, bg="white")
                row_frame.pack(fill="x", padx=15, pady=2, anchor="w")
                Label(row_frame, text=f"{key}:", font=("Arial", 11), bg="white", fg="#555555").pack(side="left", anchor="n")
                Label(row_frame, text=value, font=("Arial", 11, "bold"), bg="white", fg="#333333").pack(side="left", anchor="n")
            
            Label(detail_pendaftaran_card, text="", bg="white").pack(pady=5)

            status_pendaftaran_card = customtkinter.CTkFrame(scrollable_dashboard_frame, 
                                                             fg_color="white", corner_radius=10,
                                                             border_color="#093FB4", border_width=1)
            status_pendaftaran_card.pack(fill="x", padx=10, pady=(10, 20))

            Label(status_pendaftaran_card, text="Status Pendaftaran", 
                  font=("Helvetica", 16, "bold"), bg="white", fg="#333333").pack(padx=15, pady=(15, 5)) 
            
            current_status = "Menunggu Verifikasi" 
            status_color = "#FFA500" 
            
            if current_status == "Lulus":
                status_color = "#28a745"
            elif current_status == "Tidak Lulus":
                status_color = "#dc3545"

            status_label = Label(status_pendaftaran_card, text=f"Status Anda: {current_status}",
                                 font=("Arial", 14, "bold"), bg="white", fg=status_color)
            status_label.pack(padx=15, pady=10)
            
            Label(status_pendaftaran_card, text="Mohon tunggu informasi lebih lanjut dari admin.",
                  font=("Arial", 10), bg="white", fg="#666666").pack(padx=15, pady=(0, 15))


            persyaratan_card = customtkinter.CTkFrame(scrollable_dashboard_frame, 
                                                      fg_color="white", corner_radius=10,
                                                      border_color="#093FB4", border_width=1)
            persyaratan_card.pack(fill="x", padx=10, pady=(10, 20))

            Label(persyaratan_card, text="Persyaratan Daftar Ulang", 
                  font=("Helvetica", 16, "bold"), bg="white", fg="#333333").pack(padx=15, pady=(15, 5)) 
            
            persyaratan_text = """Siswa yang telah dinyatakan lulus wajib melakukan daftar ulang dengan membawa:
  1. Fotocopy akta kelahiran (1 lembar)

  2. Fotocopy kartu keluarga (1 lembar)

  3. Fotocopy nilai ujian sekolah dan nilai ujian nasional (1 lembar)
""" 
            Label(persyaratan_card, text=persyaratan_text, justify="left", wraplength=550,
                  font=("Arial", 11), bg="white", fg="#555555").pack(padx=15, pady=(0, 15), anchor="w")

        elif page_name == "halaman_pendaftaran":
            Label(content_frame, text="Halaman Pendaftaran Siswa", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text="Formulir untuk pendaftaran siswa baru akan dibuat di sini.", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
        elif page_name == "bukti_pendaftaran":
            Label(content_frame, text="Halaman Bukti Pendaftaran", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text="Informasi bukti pendaftaran Anda akan ditampilkan di sini.", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
            
    # Tombol-tombol Sidebar menggunakan CTkButton
    button_font = ("Arial", 12)
    button_fg_color = "#578FCA" 
    button_text_color = "white" 
    button_hover_color = "#3674B5" 
    button_corner_radius = 10 

    # Gunakan pady yang lebih kecil pada tombol pertama untuk menggesernya ke atas
    # dan pady yang konsisten antar tombol.
    # Semakin kecil nilai 50 di sini, semakin ke atas tombol "Dashboard" akan berada.
    dashboard_btn = customtkinter.CTkButton(menu_buttons_container, text="Dashboard", font=button_font, 
                                            fg_color=button_fg_color, text_color=button_text_color, 
                                            hover_color=button_hover_color, corner_radius=button_corner_radius,
                                            command=lambda: show_page("dashboard"), cursor="hand2")
    dashboard_btn.pack(pady=(50, 15), padx=10, fill="x") # UBAH NILAI INI

    halaman_pendaftaran_btn = customtkinter.CTkButton(menu_buttons_container, text="Halaman Pendaftaran", font=button_font, 
                                                       fg_color=button_fg_color, text_color=button_text_color, 
                                                       hover_color=button_hover_color, corner_radius=button_corner_radius,
                                                       command=lambda: show_page("halaman_pendaftaran"), cursor="hand2")
    halaman_pendaftaran_btn.pack(pady=15, padx=10, fill="x")

    bukti_pendaftaran_btn = customtkinter.CTkButton(menu_buttons_container, text="Bukti Pendaftaran", font=button_font, 
                                                     fg_color=button_fg_color, text_color=button_text_color, 
                                                     hover_color=button_hover_color, corner_radius=button_corner_radius,
                                                     command=lambda: show_page("bukti_pendaftaran"), cursor="hand2")
    bukti_pendaftaran_btn.pack(pady=15, padx=10, fill="x")

    logout_btn = customtkinter.CTkButton(logout_button_container, text="Logout", font=button_font, 
                                         fg_color="red", text_color="white", hover_color="#cc0000", 
                                         corner_radius=button_corner_radius,
                                         command=logout, cursor="hand2")
    logout_btn.pack(padx=10, fill="x")

    show_page("dashboard") 

    if __name__ == '__main__':
        root_test_direct = Tk()
        open_siswa_dashboard(root_test_direct, "Siswa Dummy") 
        root_test_direct.mainloop()