# modules/dashboard_siswa.py

from tkinter import *
from tkinter import messagebox, filedialog 
import customtkinter
from tkcalendar import DateEntry 
import os 
from datetime import datetime 

from . import database # Pastikan ini from . import database

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
    sidebar_frame.pack_propagate(False) 

    content_frame = Frame(main_frame, bg="#ffffff")
    content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify() 
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp 
            LoginApp(root_window) 

    def on_closing_dashboard():
        if messagebox.askyesno("Keluar", "Anda yakin ingin menutup dashboard?"):
            dashboard_siswa_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp 
            LoginApp(root_window)
            
    dashboard_siswa_window.protocol("WM_DELETE_WINDOW", on_closing_dashboard)


    welcome_label = customtkinter.CTkLabel(sidebar_frame, text=f"Selamat Datang,\n{username}!", 
                                           font=("Helvetica", 18, "bold"), text_color="white", fg_color="#093FB4",
                                           wraplength=180, justify="center")
    welcome_label.pack(pady=(20, 30), padx=10) 

    menu_buttons_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    menu_buttons_container.pack(fill="both", expand=True) 

    logout_button_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    logout_button_container.pack(fill="x", pady=(10, 20))


    def show_page(page_name):
        for widget in content_frame.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            title_label = customtkinter.CTkLabel(content_frame, text="SELAMAT DATANG CALON SISWA BARU!",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)

            scrollable_dashboard_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="transparent")
            scrollable_dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            pendaftaran_data = database.get_pendaftaran_data(username)

            detail_pendaftaran_card = customtkinter.CTkFrame(scrollable_dashboard_frame, 
                                                                 fg_color="white", corner_radius=10,
                                                                 border_color="#093FB4", border_width=1)
            detail_pendaftaran_card.pack(fill="x", padx=10, pady=(10, 20))

            Label(detail_pendaftaran_card, text="Detail Pendaftaran Anda", 
                  font=("Helvetica", 16, "bold"), bg="white", fg="#333333").pack(padx=15, pady=(15, 5)) 
            
            if pendaftaran_data:
                display_data = {
                    "Nama Lengkap": pendaftaran_data.get("nama_lengkap", "Belum Diisi"),
                    "Tempat, Tanggal Lahir": f"{pendaftaran_data.get('tempat_lahir', 'Belum Diisi')}, {pendaftaran_data.get('tanggal_lahir', 'Belum Diisi')}",
                    "Jenis Kelamin": pendaftaran_data.get("jenis_kelamin", "Belum Diisi"), # Tambah ini
                    "Asal Sekolah": pendaftaran_data.get("asal_sekolah", "Belum Diisi"),
                    "Nomor HP": pendaftaran_data.get("nomor_hp", "Belum Diisi"),
                    "Nilai Ujian Sekolah": pendaftaran_data.get("nilai_ujian_sekolah", "Belum Diisi"),
                    "Nilai Ujian Nasional": pendaftaran_data.get("nilai_ujian_nasional", "Belum Diisi")
                }
                current_status = pendaftaran_data.get("status_pendaftaran", "Belum Mendaftar")
            else:
                display_data = {
                    "Nama Lengkap": "Belum Diisi",
                    "Tempat, Tanggal Lahir": "Belum Diisi",
                    "Jenis Kelamin": "Belum Diisi", # Tambah ini
                    "Asal Sekolah": "Belum Diisi",
                    "Nomor HP": "Belum Diisi",
                    "Nilai Ujian Sekolah": "Belum Diisi",
                    "Nilai Ujian Nasional": "Belum Diisi"
                }
                current_status = "Belum Mendaftar" 

            for key, value in display_data.items():
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
            
            # --- START PERBAIKAN DI SINI ---
            status_color = "#FFA500" # Default: Oranye untuk 'Menunggu Validasi'
            status_info_text = "Mohon tunggu informasi lebih lanjut dari admin."
            
            if current_status == "Lulus":
                status_color = "#28a745" # Hijau
                status_info_text = "Selamat! Anda dinyatakan LULUS. Silakan lakukan daftar ulang sesuai persyaratan."
            elif current_status == "Tidak Lulus":
                status_color = "#dc3545" # Merah
                status_info_text = "Mohon maaf, Anda dinyatakan TIDAK LULUS. Tetap semangat!"
            elif current_status == "Ditolak": # Menambahkan kondisi ini untuk 'Ditolak'
                status_color = "#dc3545" # Biasanya warna merah sama dengan "Tidak Lulus"
                status_info_text = "Mohon maaf, pendaftaran Anda DITOLAK." 
            elif current_status == "Belum Mendaftar":
                status_color = "#6c757d" # Abu-abu
                status_info_text = "Anda belum mengisi formulir pendaftaran. Silakan isi di menu 'Halaman Pendaftaran'."
            # Jika current_status adalah "Menunggu Validasi" atau status lain yang tidak ditangkap oleh kondisi di atas,
            # maka akan tetap menggunakan nilai default yang telah diinisialisasi.
            # --- AKHIR PERBAIKAN ---

            status_label = Label(status_pendaftaran_card, text=f"Status Anda: {current_status}",
                                  font=("Arial", 14, "bold"), bg="white", fg=status_color)
            status_label.pack(padx=15, pady=10)
            
            Label(status_pendaftaran_card, text=status_info_text,
                  font=("Arial", 10), bg="white", fg="#666666", wraplength=500).pack(padx=15, pady=(0, 15))


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

4. Bukti pendaftaran online (dapat diunduh pada menu bukti pendaftaran)
""" 
            Label(persyaratan_card, text=persyaratan_text, justify="left", wraplength=550,
                  font=("Arial", 11), bg="white", fg="#555555").pack(padx=15, pady=(0, 15), anchor="w")

        elif page_name == "halaman_pendaftaran":
            title_label = customtkinter.CTkLabel(content_frame, text="FORM PENDAFTARAN",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=(20, 5))

            description_label = customtkinter.CTkLabel(content_frame, text="Silakan isi data diri Anda untuk melanjutkan pendaftaran.",
                                                       font=("Arial", 12), text_color="#333333")
            description_label.pack(pady=(0, 20))

            scrollable_form_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="transparent")
            scrollable_form_frame.pack(fill="both", expand=True, padx=10, pady=5)

            form_card = customtkinter.CTkFrame(scrollable_form_frame, 
                                               fg_color="white", corner_radius=10,
                                               border_color="#093FB4", border_width=1)
            form_card.pack(fill="x", padx=20, pady=10)

            def submit_registration():
                nama_lengkap = entry_nama_lengkap.get()
                tempat_lahir = entry_tempat_lahir.get()
                tanggal_lahir_dt = cal_tanggal_lahir.get_date()
                tanggal_lahir_str = tanggal_lahir_dt.strftime('%Y-%m-%d') 
                jenis_kelamin = gender_var.get() # Ambil nilai jenis kelamin
                asal_sekolah = entry_asal_sekolah.get()
                nomor_hp = entry_nomor_hp.get()
                
                nilai_us = entry_nilai_ujian_sekolah.get()
                nilai_un = entry_nilai_ujian_nasional.get()

                if not all([nama_lengkap, tempat_lahir, tanggal_lahir_str, jenis_kelamin, asal_sekolah, nomor_hp, nilai_us, nilai_un]): # Tambah jenis_kelamin
                    messagebox.showerror("Error", "Mohon lengkapi semua data!")
                    return
                
                try:
                    nilai_ujian_sekolah = float(nilai_us)
                    nilai_ujian_nasional = float(nilai_un)
                except ValueError:
                    messagebox.showerror("Error", "Nilai ujian harus berupa angka!")
                    return

                pendaftaran_data_to_save = {
                    "nama_lengkap": nama_lengkap,
                    "tempat_lahir": tempat_lahir,
                    "tanggal_lahir": tanggal_lahir_str,
                    "jenis_kelamin": jenis_kelamin, # Tambah ini
                    "asal_sekolah": asal_sekolah,
                    "nomor_hp": nomor_hp,
                    "nilai_ujian_sekolah": nilai_ujian_sekolah,
                    "nilai_ujian_nasional": nilai_ujian_nasional
                }
                
                success, message = database.save_pendaftaran_data(username, pendaftaran_data_to_save)
                
                if success:
                    messagebox.showinfo("Pendaftaran Berhasil", message)
                    show_page("dashboard") 
                else:
                    messagebox.showerror("Pendaftaran Gagal", message)

            def create_input_field(parent, label_text, is_date_entry=False, label_width=150): 
                frame = customtkinter.CTkFrame(parent, fg_color="transparent")
                frame.pack(fill="x", pady=5, padx=15) 

                frame.grid_columnconfigure(0, weight=0) 
                frame.grid_columnconfigure(1, weight=1) 

                label = customtkinter.CTkLabel(frame, text=label_text, font=("Arial", 11, "bold"), text_color="#333333",
                                               width=label_width, anchor="w") 
                label.grid(row=0, column=0, sticky="w", padx=(0, 10)) 

                if is_date_entry:
                    date_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
                    date_frame.grid(row=0, column=1, sticky="ew") 

                    date_entry_widget = DateEntry(date_frame, selectmode='day', font=("Arial", 11),
                                                 date_pattern='dd-mm-yyyy', background="#2074B4", 
                                                 foreground="white", bordercolor="#093FB4",
                                                 headersbackground="#093FB4", headersforeground="white",
                                                 normalbackground="white", normalforeground="black")
                    date_entry_widget.pack(fill="x", expand=True) 
                    return date_entry_widget 

                else:
                    entry = customtkinter.CTkEntry(frame, font=("Arial", 11), 
                                                 fg_color="#f0f0f0", text_color="#333333",
                                                 border_color="#cccccc", border_width=1, corner_radius=5)
                    entry.grid(row=0, column=1, sticky="ew") 
                    return entry

            entry_nama_lengkap = create_input_field(form_card, "Nama Lengkap:")
            entry_tempat_lahir = create_input_field(form_card, "Tempat Lahir:")
            cal_tanggal_lahir = create_input_field(form_card, "Tanggal Lahir:", is_date_entry=True)
            
            # --- Tambahkan input jenis kelamin di sini ---
            gender_frame = customtkinter.CTkFrame(form_card, fg_color="transparent")
            gender_frame.pack(fill="x", pady=5, padx=15)
            gender_frame.grid_columnconfigure(0, weight=0)
            gender_frame.grid_columnconfigure(1, weight=1)
            customtkinter.CTkLabel(gender_frame, text="Jenis Kelamin:", font=("Arial", 11, "bold"), text_color="#333333",
                                   width=150, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
            
            gender_options = ["Laki-laki", "Perempuan"]
            gender_var = StringVar(value="") # Variabel untuk menyimpan pilihan
            
            gender_optionmenu = customtkinter.CTkOptionMenu(gender_frame, values=gender_options,
                                                            variable=gender_var,
                                                            fg_color="#f0f0f0", button_color="#093FB4",
                                                            button_hover_color="#07308D", text_color="#333333")
            gender_optionmenu.grid(row=0, column=1, sticky="ew")
            # --- Akhir penambahan jenis kelamin ---

            entry_asal_sekolah = create_input_field(form_card, "Asal Sekolah:")
            entry_nomor_hp = create_input_field(form_card, "Nomor HP:")
            entry_nilai_ujian_sekolah = create_input_field(form_card, "Nilai Ujian Sekolah:")
            entry_nilai_ujian_nasional = create_input_field(form_card, "Nilai Ujian Nasional:")

            def load_existing_pendaftaran_data():
                data_from_db = database.get_pendaftaran_data(username)
                if data_from_db:
                    entry_nama_lengkap.insert(0, data_from_db.get("nama_lengkap", ""))
                    entry_tempat_lahir.insert(0, data_from_db.get("tempat_lahir", ""))
                    
                    try:
                        tanggal_dt = datetime.strptime(data_from_db.get("tanggal_lahir", ""), '%Y-%m-%d')
                        cal_tanggal_lahir.set_date(tanggal_dt)
                    except ValueError:
                        pass
                    
                    # Set nilai jenis kelamin jika ada
                    if data_from_db.get("jenis_kelamin"):
                        gender_var.set(data_from_db.get("jenis_kelamin"))
                        
                    entry_asal_sekolah.insert(0, data_from_db.get("asal_sekolah", ""))
                    entry_nomor_hp.insert(0, data_from_db.get("nomor_hp", ""))
                    entry_nilai_ujian_sekolah.insert(0, str(data_from_db.get("nilai_ujian_sekolah", "")))
                    entry_nilai_ujian_nasional.insert(0, str(data_from_db.get("nilai_ujian_nasional", "")))
            
            dashboard_siswa_window.after(100, load_existing_pendaftaran_data)

            register_btn = customtkinter.CTkButton(form_card, text="Daftar", font=("Arial", 14, "bold"),
                                                 fg_color="#093FB4", text_color="white", 
                                                 hover_color="#07308D", corner_radius=10,
                                                 command=submit_registration, cursor="hand2")
            register_btn.pack(pady=(20, 15), padx=15, fill="x") 
            
        elif page_name == "bukti_pendaftaran":
            title_label = customtkinter.CTkLabel(content_frame, text="UNDUH BUKTI PENDAFTARAN",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=(20, 5))

            description_label = customtkinter.CTkLabel(content_frame, text="Unduh bukti pendaftaran sebagai syarat daftar ulang.",
                                                       font=("Arial", 12), text_color="#333333")
            description_label.pack(pady=(0, 20))

            bukti_card = customtkinter.CTkFrame(content_frame, 
                                                     fg_color="white", corner_radius=10,
                                                     border_color="#093FB4", border_width=1)
            bukti_card.pack(fill="x", padx=20, pady=10)

            bukti_content_frame = customtkinter.CTkFrame(bukti_card, fg_color="transparent")
            bukti_content_frame.pack(fill="x", padx=15, pady=15)
            
            bukti_content_frame.grid_columnconfigure(0, weight=1) 
            bukti_content_frame.grid_columnconfigure(1, weight=0) 

            file_name_label = customtkinter.CTkLabel(bukti_content_frame, text="Bukti_Pendaftaran_Siswa.pdf",
                                                     font=("Arial", 12, "bold"), text_color="#333333")
            file_name_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

            def download_bukti():
                pendaftaran_data = database.get_pendaftaran_data(username)

                if not pendaftaran_data or pendaftaran_data.get("status_pendaftaran") == "Belum Mendaftar":
                    messagebox.showwarning("Belum Terdaftar", "Anda belum mengisi data pendaftaran. Silakan isi terlebih dahulu.")
                    return
                
                # Membuka dialog simpan file
                initial_filename = f"Bukti_Pendaftaran_{username}.pdf"
                file_path = filedialog.asksaveasfilename(
                     defaultextension=".pdf",
                    initialfile=initial_filename,
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Simpan Bukti Pendaftaran"
                )

                if file_path: # Jika user memilih lokasi dan nama file
                    try:
                        # Panggil fungsi generate PDF dari modul database
                        success = database.generate_bukti_pendaftaran_pdf(file_path, username, pendaftaran_data)
                        if success:
                            messagebox.showinfo("Unduh Berhasil", f"File '{os.path.basename(file_path)}' berhasil dibuat di:\n{os.path.dirname(file_path)}")
                            # Opsi untuk membuka file PDF secara otomatis (tergantung OS dan viewer)
                            # os.startfile(file_path) # Hanya untuk Windows, butuh penanganan lintas OS
                        else:
                            messagebox.showerror("Unduh Gagal", "Terjadi kesalahan saat membuat file PDF.")
                    except Exception as e:
                        messagebox.showerror("Error Unduh", f"Terjadi kesalahan: {e}")
                else:
                    messagebox.showinfo("Unduh Dibatalkan", "Pengunduhan dibatalkan.")


            download_btn = customtkinter.CTkButton(bukti_content_frame, text="Unduh", font=("Arial", 12, "bold"),
                                                 fg_color="#28a745", text_color="white", 
                                                 hover_color="#218838", corner_radius=5,
                                                 command=download_bukti, cursor="hand2")
            download_btn.grid(row=0, column=1, sticky="e")
            
    button_font = ("Arial", 12)
    button_fg_color = "#578FCA" 
    button_text_color = "white" 
    button_hover_color = "#3674B5" 
    button_corner_radius = 10 

    dashboard_btn = customtkinter.CTkButton(menu_buttons_container, text="Dashboard", font=button_font, 
                                            fg_color=button_fg_color, text_color=button_text_color, 
                                            hover_color=button_hover_color, corner_radius=button_corner_radius,
                                            command=lambda: show_page("dashboard"), cursor="hand2")
    dashboard_btn.pack(pady=(50, 15), padx=10, fill="x") 

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
        database.create_tables() 
        if not database.get_user_by_username("siswa_test"):
            database.register_user("test@example.com", "siswa_test", "password")
        
        root_test_direct = Tk()
        open_siswa_dashboard(root_test_direct, "siswa_test") 
        root_test_direct.mainloop()