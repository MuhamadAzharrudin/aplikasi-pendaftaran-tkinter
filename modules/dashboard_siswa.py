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

    # --- Logout Function (DIPINDAHKAN KE ATAS) ---
    # Define it before it's used by the button
    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify() 
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp 
            LoginApp(root_window) 

    # --- Protocol untuk menangani penutupan jendela dashboard (DIPINDAHKAN KE ATAS) ---
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
                                  font=("Helvetica", 14, "bold"), text_color="white", fg_color="#093FB4",
                                  wraplength=180, justify="center")
    welcome_label.pack(pady=(20, 30), padx=10) # Padding bawah lebih besar

    # --- Frame untuk Tombol-Tombol Menu Utama ---
    menu_buttons_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    menu_buttons_container.pack(fill="both", expand=True) 

    # --- Frame untuk Tombol Logout ---
    logout_button_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    logout_button_container.pack(fill="x", pady=(10, 20))


    # Fungsi untuk menampilkan konten di content_frame (tetap sama)
    def show_page(page_name):
        for widget in content_frame.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            Label(content_frame, text="Halaman Dashboard Siswa", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text="Ringkasan informasi penting Anda.", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
        elif page_name == "edit_nilai":
            Label(content_frame, text="Halaman Edit Nilai", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text="Di sini Anda bisa melihat dan mengedit nilai (jika diizinkan).", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
        elif page_name == "profil":
            Label(content_frame, text="Halaman Profil Siswa", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text=f"Nama Pengguna: {username}\nEmail: (Ambil dari Database)", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
        elif page_name == "bukti_pendaftaran":
            Label(content_frame, text="Halaman Bukti Pendaftaran", 
                  font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333").pack(pady=50)
            Label(content_frame, text="Informasi bukti pendaftaran Anda.", 
                  font=("Arial", 12), bg="#ffffff", fg="#666666").pack(pady=10)
            
    # Tombol-tombol Sidebar menggunakan CTkButton
    button_font = ("Arial", 12)
    button_fg_color = "#578FCA" # Warna latar belakang tombol
    button_text_color = "white" # Warna teks tombol
    button_hover_color = "#3674B5" # Warna saat di-hover
    button_corner_radius = 10 # Radius untuk efek rounded

    dashboard_btn = customtkinter.CTkButton(menu_buttons_container, text="Dashboard", font=button_font, 
                                            fg_color=button_fg_color, text_color=button_text_color, 
                                            hover_color=button_hover_color, corner_radius=button_corner_radius,
                                            command=lambda: show_page("dashboard"), cursor="hand2")
    dashboard_btn.pack(pady=5, padx=10, fill="x")

    edit_nilai_btn = customtkinter.CTkButton(menu_buttons_container, text="Edit Nilai", font=button_font, 
                                             fg_color=button_fg_color, text_color=button_text_color, 
                                             hover_color=button_hover_color, corner_radius=button_corner_radius,
                                             command=lambda: show_page("edit_nilai"), cursor="hand2")
    edit_nilai_btn.pack(pady=5, padx=10, fill="x")

    profil_btn = customtkinter.CTkButton(menu_buttons_container, text="Profil", font=button_font, 
                                         fg_color=button_fg_color, text_color=button_text_color, 
                                         hover_color=button_hover_color, corner_radius=button_corner_radius,
                                         command=lambda: show_page("profil"), cursor="hand2")
    profil_btn.pack(pady=5, padx=10, fill="x")

    bukti_pendaftaran_btn = customtkinter.CTkButton(menu_buttons_container, text="Bukti Pendaftaran", font=button_font, 
                                                     fg_color=button_fg_color, text_color=button_text_color, 
                                                     hover_color=button_hover_color, corner_radius=button_corner_radius,
                                                     command=lambda: show_page("bukti_pendaftaran"), cursor="hand2")
    bukti_pendaftaran_btn.pack(pady=5, padx=10, fill="x")

    # Tombol Logout (di-pack ke logout_button_container)
    logout_btn = customtkinter.CTkButton(logout_button_container, text="Logout", font=button_font, 
                                         fg_color="red", text_color="white", hover_color="#cc0000", 
                                         corner_radius=button_corner_radius,
                                         command=logout, cursor="hand2") # <-- logout is now defined above
    logout_btn.pack(padx=10, fill="x") # pady sudah diatur di container-nya

    show_page("dashboard")

    if __name__ == '__main__':
        root_test_direct = Tk()
        open_siswa_dashboard(root_test_direct, "Siswa Dummy") 
        root_test_direct.mainloop()