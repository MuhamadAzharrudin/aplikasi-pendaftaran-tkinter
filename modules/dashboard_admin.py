# modules/dashboard_admin.py

from tkinter import *
from tkinter import messagebox, filedialog 
from tkinter import ttk
import customtkinter
import os 
from datetime import datetime
import csv 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer # Import Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # Import ParagraphStyle
from reportlab.lib.enums import TA_CENTER # Import TA_CENTER for alignment


# Import modul database yang sudah ada
from . import database 

# Global dictionary untuk melacak status checkbox
# Kunci: Treeview item ID, Nilai: IntVar()
checked_items = {}

# Fungsi utama untuk membuka dashboard admin
def open_admin_dashboard(root_window, username):
    dashboard_admin_window = Toplevel(root_window)
    dashboard_admin_window.title(f"Dashboard Admin - {username}")
    dashboard_admin_window.geometry("1000x600+100+50")
    dashboard_admin_window.configure(bg="#f0f0f0")
    dashboard_admin_window.resizable(True, True)

    root_window.withdraw()

    main_frame = customtkinter.CTkFrame(dashboard_admin_window, fg_color="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=5, pady=5) 

    sidebar_frame = customtkinter.CTkFrame(main_frame, width=220, corner_radius=10, fg_color="#093FB4")
    sidebar_frame.pack(side="left", fill="y", padx=(5, 0), pady=5) 
    sidebar_frame.pack_propagate(False) 

    content_frame = customtkinter.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=10)
    content_frame.pack(side="right", fill="both", expand=True, padx=(0, 5), pady=5) 

    def logout():
        if messagebox.askyesno("Logout", "Anda yakin ingin keluar?"):
            dashboard_admin_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp
            LoginApp(root_window)

    def on_closing_dashboard():
        if messagebox.askyesno("Keluar", "Anda yakin ingin menutup dashboard?"):
            dashboard_admin_window.destroy()
            root_window.deiconify()
            for widget in root_window.winfo_children():
                widget.destroy()
            from modules.login import LoginApp
            LoginApp(root_window)
            
    dashboard_admin_window.protocol("WM_DELETE_WINDOW", on_closing_dashboard)

    title_bar_frame = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent")
    title_bar_frame.pack(pady=(20, 10), padx=10, fill="x")

    title_label = customtkinter.CTkLabel(title_bar_frame, text="DASHBOARD ADMIN",
                                         font=("Helvetica", 20, "bold"), text_color="white",
                                         wraplength=200, justify="center")
    title_label.pack(expand=True)

    welcome_label = customtkinter.CTkLabel(sidebar_frame, text=f"Selamat Datang,\n{username}!",
                                         font=("Helvetica", 16), text_color="white", 
                                         wraplength=180, justify="center")
    welcome_label.pack(pady=(10, 30), padx=10)

    menu_buttons_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    menu_buttons_container.pack(fill="both", expand=True)

    logout_button_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
    logout_button_container.pack(fill="x", pady=(10, 20))

    # --- Fungsi untuk menampilkan halaman yang berbeda di content_frame ---
    def show_page(page_name):
        for widget in content_frame.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            title_label = customtkinter.CTkLabel(content_frame, text="DATA PENDAFTAR CALON SISWA BARU",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)
            
            # Mendapatkan data dari database
            total_pendaftar = database.get_total_pendaftar()
            pendaftar_lolos = database.get_pendaftar_by_status("Lulus")
            
            # Card Pendaftar Masuk
            card_frame_top = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            card_frame_top.pack(fill="x", padx=20, pady=10)
            
            card_pendaftar_masuk = customtkinter.CTkFrame(card_frame_top, fg_color="white", corner_radius=10,
                                                          border_color="#2196F3", border_width=2) # Biru untuk pendaftar masuk
            card_pendaftar_masuk.pack(side="left", fill="both", expand=True, padx=(0, 10))

            customtkinter.CTkLabel(card_pendaftar_masuk, text="PENDAFTAR MASUK",
                                   font=("Helvetica", 16, "bold"), text_color="#2196F3").pack(pady=(15, 5))
            customtkinter.CTkLabel(card_pendaftar_masuk, text=f"{total_pendaftar} Orang",
                                   font=("Helvetica", 28, "bold"), text_color="#333333").pack(pady=(0, 10))
            
            progress_bar_pendaftar = customtkinter.CTkProgressBar(card_pendaftar_masuk, fg_color="#e0e0e0", progress_color="#2196F3")
            progress_bar_pendaftar.pack(fill="x", padx=15, pady=(0, 15))
            progress_bar_pendaftar.set(1.0) # Selalu penuh karena menunjukkan total pendaftar
            
            # Card Lolos Seleksi
            card_lolos_seleksi = customtkinter.CTkFrame(card_frame_top, fg_color="white", corner_radius=10,
                                                         border_color="#4CAF50", border_width=2) # Hijau untuk lolos seleksi
            card_lolos_seleksi.pack(side="right", fill="both", expand=True, padx=(10, 0))

            customtkinter.CTkLabel(card_lolos_seleksi, text="LOLOS SELEKSI",
                                   font=("Helvetica", 16, "bold"), text_color="#4CAF50").pack(pady=(15, 5))
            customtkinter.CTkLabel(card_lolos_seleksi, text=f"{len(pendaftar_lolos)} Orang",
                                   font=("Helvetica", 28, "bold"), text_color="#333333").pack(pady=(0, 10))

            progress_bar_lolos = customtkinter.CTkProgressBar(card_lolos_seleksi, fg_color="#e0e0e0", progress_color="#4CAF50")
            progress_bar_lolos.pack(fill="x", padx=15, pady=(0, 15))
            if total_pendaftar > 0:
                progress_bar_lolos.set(len(pendaftar_lolos) / total_pendaftar)
            else:
                progress_bar_lolos.set(0)

            # Bagian Data Pendaftar yang Masuk (Tabel)
            data_pendaftar_label = customtkinter.CTkLabel(content_frame, text="Data Pendaftar yang Masuk:",
                                                          font=("Helvetica", 16, "bold"), text_color="#333333")
            data_pendaftar_label.pack(pady=(20, 10), anchor="w", padx=20)

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#093FB4", foreground="white")
            style.configure("Treeview", font=("Arial", 10), rowheight=25)
            style.map("Treeview", background=[('selected', '#578FCA')])

            tree_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

            tree_scroll_y = Scrollbar(tree_frame, orient="vertical")
            tree_scroll_y.pack(side="right", fill="y")
            tree_scroll_x = Scrollbar(tree_frame, orient="horizontal")
            tree_scroll_x.pack(side="bottom", fill="x")

            tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="browse") 
            tree.pack(fill="both", expand=True)

            tree_scroll_y.config(command=tree.yview)
            tree_scroll_x.config(command=tree.xview)

            tree["columns"] = ("No", "Nama", "Alamat", "Nilai UN", "Nilai US", "Rata-Rata", "Status")
            tree.column("#0", width=0, stretch=NO) 
            tree.column("No", anchor=CENTER, width=40)
            tree.column("Nama", anchor=W, width=150) 
            tree.column("Alamat", anchor=W, width=250) # Untuk alamat lebih luas
            tree.column("Nilai UN", anchor=CENTER, width=80)
            tree.column("Nilai US", anchor=CENTER, width=80)
            tree.column("Rata-Rata", anchor=CENTER, width=100)
            tree.column("Status", anchor=CENTER, width=120)

            tree.heading("#0", text="", anchor=CENTER)
            tree.heading("No", text="No", anchor=CENTER)
            tree.heading("Nama", text="Nama", anchor=CENTER)
            tree.heading("Alamat", text="Alamat", anchor=CENTER)
            tree.heading("Nilai UN", text="Nilai UN", anchor=CENTER)
            tree.heading("Nilai US", text="Nilai US", anchor=CENTER)
            tree.heading("Rata-Rata", text="Rata-Rata", anchor=CENTER)
            tree.heading("Status", text="Status", anchor=CENTER)

            def load_dashboard_pendaftar_data():
                for item in tree.get_children():
                    tree.delete(item)
                
                all_pendaftar_data = database.get_all_pendaftar_data() # Mengambil semua data pendaftar

                for i, pendaftar in enumerate(all_pendaftar_data):
                    nama = pendaftar.get("nama_lengkap", "N/A")
                    # Untuk alamat, kita bisa gabungkan tempat lahir dan asal sekolah sebagai placeholder
                    alamat = f"{pendaftar.get('tempat_lahir', '')}, {pendaftar.get('asal_sekolah', '')}"
                    nilai_un = pendaftar.get("nilai_ujian_nasional", 0.0)
                    nilai_us = pendaftar.get("nilai_ujian_sekolah", 0.0)
                    
                    rata_rata = (nilai_un + nilai_us) / 2 if (nilai_un is not None and nilai_us is not None) else 0.0
                    status = pendaftar.get("status_pendaftaran", "Belum Validasi")
                    
                    # Menyesuaikan teks status
                    display_status = status 
                    if status == "Menunggu Validasi":
                        display_status = "Calon Siswa Baru" # Sesuai gambar
                    elif status == "Lulus":
                        display_status = "Lolos Seleksi"
                    elif status == "Tidak Lulus":
                        display_status = "Tidak Lolos"
                    elif status == "Ditolak":
                        display_status = "Ditolak Admin"

                    tree.insert("", END, values=(
                        i + 1, 
                        nama, 
                        alamat, 
                        nilai_un, 
                        nilai_us, 
                        f"{rata_rata:.2f}", # Format rata-rata 2 angka di belakang koma
                        display_status
                    ))
            
            load_dashboard_pendaftar_data()

        elif page_name == "validasi_data":
            title_label = customtkinter.CTkLabel(content_frame, text="VALIDASI DATA PENDAFTAR",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)
            
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#093FB4", foreground="white")
            style.configure("Treeview", font=("Arial", 10), rowheight=25)
            style.map("Treeview", background=[('selected', '#578FCA')])

            tree_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

            tree_scroll_y = Scrollbar(tree_frame, orient="vertical")
            tree_scroll_y.pack(side="right", fill="y")
            tree_scroll_x = Scrollbar(tree_frame, orient="horizontal")
            tree_scroll_x.pack(side="bottom", fill="x")

            tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="browse") 
            tree.pack(fill="both", expand=True)

            tree_scroll_y.config(command=tree.yview)
            tree_scroll_x.config(command=tree.xview)

            tree["columns"] = ("Pilih", "ID", "Username", "Nama Lengkap", "Asal Sekolah", "Nilai US", "Nilai UN", "Status")
            tree.column("#0", width=0, stretch=NO) 
            tree.column("Pilih", anchor=CENTER, width=50, minwidth=50, stretch=NO)
            tree.column("ID", anchor=CENTER, width=50)
            tree.column("Username", anchor=W, width=100) 
            tree.column("Nama Lengkap", anchor=W, width=150)
            tree.column("Asal Sekolah", anchor=W, width=150)
            tree.column("Nilai US", anchor=CENTER, width=80)
            tree.column("Nilai UN", anchor=CENTER, width=80)
            tree.column("Status", anchor=CENTER, width=120)

            tree.heading("#0", text="", anchor=CENTER)
            tree.heading("Pilih", text="✔", anchor=CENTER) 
            tree.heading("ID", text="ID", anchor=CENTER)
            tree.heading("Username", text="Username", anchor=CENTER)
            tree.heading("Nama Lengkap", text="Nama Lengkap", anchor=CENTER)
            tree.heading("Asal Sekolah", text="Asal Sekolah", anchor=CENTER)
            tree.heading("Nilai US", text="Nilai US", anchor=CENTER)
            tree.heading("Nilai UN", text="Nilai UN", anchor=CENTER)
            tree.heading("Status", text="Status", anchor=CENTER)

            def toggle_checkbox(item_id):
                if item_id in checked_items:
                    current_value = checked_items[item_id].get()
                    new_value = 1 - current_value 
                    checked_items[item_id].set(new_value) 
                    tree.set(item_id, "Pilih", "✔" if new_value == 1 else "")
                else:
                    print(f"Warning: Item ID {item_id} not found in checked_items.")

            def on_tree_click(event):
                item_id = tree.identify_row(event.y)
                if item_id:
                    column = tree.identify_column(event.x)
                    if column == "#1" or (column != "#0" and tree.identify_region(event.x, event.y) == "cell"):
                        toggle_checkbox(item_id)
                
                region = tree.identify("region", event.x, event.y)
                if region == "heading":
                    column = tree.identify_column(event.x)
                    if column == "#1": 
                        toggle_all_checkboxes()

            tree.bind("<ButtonRelease-1>", on_tree_click)

            def toggle_all_checkboxes():
                all_checked = all(var.get() == 1 for var in checked_items.values())
                new_state = 0 if all_checked else 1 

                for item_id, var in checked_items.items():
                    var.set(new_state)
                    tree.set(item_id, "Pilih", "✔" if new_state == 1 else "")

            def load_pendaftar_data():
                global checked_items 
                
                for item in tree.get_children():
                    tree.delete(item)
                checked_items.clear() 
                
                conn = database.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, nama_lengkap, asal_sekolah, nilai_ujian_sekolah, nilai_ujian_nasional, status_pendaftaran FROM pendaftar")
                rows = cursor.fetchall()
                conn.close()

                for row in rows:
                    item_id = tree.insert("", END, values=(
                        "", 
                        row["id"], 
                        row["username"], 
                        row["nama_lengkap"], 
                        row["asal_sekolah"], 
                        row["nilai_ujian_sekolah"], 
                        row["nilai_ujian_nasional"], 
                        row["status_pendaftaran"]
                    ))
                    checked_items[item_id] = IntVar(value=0) 
                    tree.set(item_id, "Pilih", "") 

            def get_selected_pendaftar_usernames():
                selected_usernames = []
                for item_id, var in checked_items.items():
                    if var.get() == 1: 
                        username = tree.item(item_id, "values")[2] 
                        selected_usernames.append(username)
                return selected_usernames

            def update_selected_status(status):
                selected_usernames = get_selected_pendaftar_usernames()
                if not selected_usernames:
                    messagebox.showwarning("Peringatan", "Pilih setidaknya satu pendaftar yang ingin divalidasi/ditolak menggunakan checkbox.")
                    return
                
                if messagebox.askyesno("Konfirmasi", f"Anda yakin ingin mengubah status {len(selected_usernames)} pendaftar menjadi '{status}'?"):
                    conn = database.get_db_connection()
                    cursor = conn.cursor()
                    for username in selected_usernames:
                        cursor.execute("UPDATE pendaftar SET status_pendaftaran = ? WHERE username = ?", (status, username))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Berhasil", f"Status {len(selected_usernames)} pendaftar berhasil diubah menjadi '{status}'.")
                    load_pendaftar_data() 

            def delete_selected_pendaftar():
                selected_usernames = get_selected_pendaftar_usernames()
                if not selected_usernames:
                    messagebox.showwarning("Peringatan", "Pilih setidaknya satu pendaftar yang ingin dihapus menggunakan checkbox.")
                    return
                
                if messagebox.askyesno("Konfirmasi Hapus", f"Anda yakin ingin MENGHAPUS {len(selected_usernames)} data pendaftar yang dipilih secara permanen?"):
                    conn = database.get_db_connection()
                    cursor = conn.cursor()
                    for username in selected_usernames:
                        # HANYA HAPUS DARI TABEL 'pendaftar'
                        cursor.execute("DELETE FROM pendaftar WHERE username = ?", (username,))
                        # Baris di bawah ini yang DIHAPUS agar akun user tidak terhapus
                        # cursor.execute("DELETE FROM users WHERE username = ?", (username,)) 
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Berhasil", f"{len(selected_usernames)} data pendaftar berhasil dihapus dari daftar pendaftar.")
                    load_pendaftar_data() 

            def toggle_all_checkboxes_manual(state):
                for item_id, var in checked_items.items():
                    var.set(state)
                    tree.set(item_id, "Pilih", "✔" if state == 1 else "")

            load_pendaftar_data() 

            button_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            button_frame.pack(pady=10)

            validate_btn = customtkinter.CTkButton(button_frame, text="LULUSKAN (Terpilih)",
                                                   fg_color="green", hover_color="#006400",
                                                   command=lambda: update_selected_status("Lulus"), cursor="hand2")
            validate_btn.pack(side="left", padx=10)

            reject_btn = customtkinter.CTkButton(button_frame, text="TOLAK (Terpilih)",
                                                   fg_color="red", hover_color="#8B0000",
                                                   command=lambda: update_selected_status("Ditolak"), cursor="hand2")
            reject_btn.pack(side="left", padx=10)

            delete_btn = customtkinter.CTkButton(button_frame, text="HAPUS (Terpilih)",
                                                   fg_color="darkred", hover_color="#8B0000",
                                                   command=delete_selected_pendaftar, cursor="hand2")
            delete_btn.pack(side="left", padx=10)

            refresh_btn = customtkinter.CTkButton(button_frame, text="Refresh Data",
                                                   fg_color="#578FCA", hover_color="#3674B5",
                                                   command=load_pendaftar_data, cursor="hand2")
            refresh_btn.pack(side="left", padx=10)
            
            
        elif page_name == "laporan":
            title_label = customtkinter.CTkLabel(content_frame, text="LAPORAN PENDAFTARAN",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#093FB4", foreground="white")
            style.configure("Treeview", font=("Arial", 10), rowheight=25)
            style.map("Treeview", background=[('selected', '#578FCA')])

            tree_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

            tree_scroll_y = Scrollbar(tree_frame, orient="vertical")
            tree_scroll_y.pack(side="right", fill="y")
            tree_scroll_x = Scrollbar(tree_frame, orient="horizontal")
            tree_scroll_x.pack(side="bottom", fill="x")

            tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="browse") 
            tree.pack(fill="both", expand=True)

            tree_scroll_y.config(command=tree.yview)
            tree_scroll_x.config(command=tree.xview)

            tree["columns"] = ("No", "Nama", "Jenis Kelamin", "Nilai UN", "Nilai US", "Rata-Rata", "Status")
            tree.column("#0", width=0, stretch=NO) 
            tree.column("No", anchor=CENTER, width=40)
            tree.column("Nama", anchor=W, width=180) 
            tree.column("Jenis Kelamin", anchor=CENTER, width=100)
            tree.column("Nilai UN", anchor=CENTER, width=90)
            tree.column("Nilai US", anchor=CENTER, width=90)
            tree.column("Rata-Rata", anchor=CENTER, width=100)
            tree.column("Status", anchor=CENTER, width=120)

            tree.heading("#0", text="", anchor=CENTER)
            tree.heading("No", text="No", anchor=CENTER)
            tree.heading("Nama", text="Nama", anchor=CENTER)
            tree.heading("Jenis Kelamin", text="Jenis Kelamin", anchor=CENTER)
            tree.heading("Nilai UN", text="Nilai UN", anchor=CENTER)
            tree.heading("Nilai US", text="Nilai US", anchor=CENTER)
            tree.heading("Rata-Rata", text="Rata-Rata", anchor=CENTER)
            tree.heading("Status", text="Status", anchor=CENTER)

            def load_report_data():
                for item in tree.get_children():
                    tree.delete(item)
                
                # Mengambil semua data pendaftar
                all_pendaftar_data = database.get_all_pendaftar_data()

                # Pisahkan data berdasarkan status
                lolos_seleksi = [p for p in all_pendaftar_data if p.get("status_pendaftaran") == "Lulus"]
                tidak_lolos = [p for p in all_pendaftar_data if p.get("status_pendaftaran") == "Tidak Lulus"]
                belum_validasi = [p for p in all_pendaftar_data if p.get("status_pendaftaran") == "Menunggu Validasi" or p.get("status_pendaftaran") == "Belum Validasi"]
                ditolak_admin = [p for p in all_pendaftar_data if p.get("status_pendaftaran") == "Ditolak"]

                # Urutkan berdasarkan status: Lulus, Tidak Lulus, Belum Validasi, Ditolak
                sorted_pendaftar = lolos_seleksi + tidak_lolos + belum_validasi + ditolak_admin
                
                for i, pendaftar in enumerate(sorted_pendaftar):
                    nama = pendaftar.get("nama_lengkap", "N/A")
                    jenis_kelamin = pendaftar.get("jenis_kelamin", "N/A")
                    nilai_un = pendaftar.get("nilai_ujian_nasional", 0.0)
                    nilai_us = pendaftar.get("nilai_ujian_sekolah", 0.0)
                    
                    rata_rata = (nilai_un + nilai_us) / 2 if (nilai_un is not None and nilai_us is not None) else 0.0
                    status = pendaftar.get("status_pendaftaran", "Belum Validasi")

                    # Menyesuaikan teks status untuk laporan
                    display_status = status 
                    if status == "Menunggu Validasi":
                        display_status = "Belum Divalidasi"
                    elif status == "Lulus":
                        display_status = "Lolos Seleksi"
                    elif status == "Tidak Lulus":
                        display_status = "Tidak Lolos"
                    elif status == "Ditolak":
                        display_status = "Ditolak Admin"

                    tree.insert("", END, values=(
                        i + 1, 
                        nama, 
                        jenis_kelamin, 
                        nilai_un, 
                        nilai_us, 
                        f"{rata_rata:.2f}", 
                        display_status
                    ))
            
            load_report_data()

            def export_data_to_csv():
                # Mengubah nama file default
                initial_filename = f"Laporan_pendaftaran_2025.csv"
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    initialfile=initial_filename,
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Simpan Laporan Pendaftar (CSV)"
                )

                if file_path: # Jika user memilih lokasi dan nama file
                    try:
                        with open(file_path, 'w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write header
                            header = [tree.heading(col)["text"] for col in tree["columns"]]
                            writer.writerow(header)
                            # Write data
                            for item_id in tree.get_children():
                                writer.writerow(tree.item(item_id, "values"))
                        messagebox.showinfo("Ekspor Berhasil", f"Data berhasil diekspor ke:\n{file_path}")
                    except Exception as e:
                        messagebox.showerror("Ekspor Gagal", f"Terjadi kesalahan saat mengekspor data CSV: {e}")
                else:
                    messagebox.showinfo("Ekspor Dibatalkan", "Ekspor CSV dibatalkan.")


            def export_data_to_pdf():
                # Mengubah nama file default
                initial_filename = f"Laporan_pendaftaran_2025.pdf"
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    initialfile=initial_filename,
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Simpan Laporan Pendaftar (PDF)"
                )

                if file_path: # Jika user memilih lokasi dan nama file
                    doc = SimpleDocTemplate(file_path, pagesize=letter) 
                    styles = getSampleStyleSheet()
                    
                    # Custom style for header
                    header_style_title = ParagraphStyle(
                        name='HeaderTitle',
                        parent=styles['h2'], # Inherit from h2 for size
                        fontName='Helvetica-Bold',
                        fontSize=16,
                        alignment=TA_CENTER,
                        spaceAfter=6
                    )
                    header_style_subtitle = ParagraphStyle(
                        name='HeaderSubtitle',
                        parent=styles['h3'], # Inherit from h3 for size
                        fontName='Helvetica-Bold',
                        fontSize=12,
                        alignment=TA_CENTER,
                        spaceAfter=4
                    )
                    header_style_address = ParagraphStyle(
                        name='HeaderAddress',
                        parent=styles['Normal'],
                        fontName='Helvetica',
                        fontSize=10,
                        alignment=TA_CENTER,
                        spaceAfter=12
                    )

                    elements = []

                    # Add header content
                    elements.append(Paragraph("LAPORAN PENDAFTARAN CALON PESERTA DIDIK BARU", header_style_title))
                    elements.append(Paragraph("SMA NEGERI 1 AIKMEL", header_style_subtitle))
                    elements.append(Paragraph("Jalan Pendidikan Nomor 88 Kec. Aikmel, Kab. Lombok Timur", header_style_address))
                    elements.append(Spacer(1, 12)) # Add some space after header

                    data = []
                    # Add table header
                    header_table = [Paragraph(tree.heading(col)["text"], styles['h5']) for col in tree["columns"]]
                    data.append(header_table)
                    
                    # Add data rows
                    for item_id in tree.get_children():
                        row_values = tree.item(item_id, "values")
                        data.append([Paragraph(str(val), styles['Normal']) for val in row_values])

                    # Table style
                    table_style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#093FB4")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0,0), (-1,-1), 8), # Smaller font size for data
                    ])

                    # Apply alternating row colors
                    for i in range(1, len(data)):
                        if i % 2 == 0:
                            table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f0f0f0"))

                    table = Table(data)
                    table.setStyle(table_style)
                    elements.append(table) # Add the table to the elements list

                    try:
                        doc.build(elements) # Build the document with all elements
                        messagebox.showinfo("Ekspor Berhasil", f"Data berhasil diekspor ke:\n{file_path}")
                    except Exception as e:
                        messagebox.showerror("Ekspor Gagal", f"Terjadi kesalahan saat mengekspor data PDF: {e}")
                else:
                    messagebox.showinfo("Ekspor Dibatalkan", "Ekspor PDF dibatalkan.")


            report_buttons_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
            report_buttons_frame.pack(pady=10)

            cetak_data_btn = customtkinter.CTkButton(report_buttons_frame, text="Cetak Data Pendaftar (PDF)",
                                                    fg_color="#E67E22", hover_color="#D35400",
                                                    command=export_data_to_pdf, cursor="hand2")
            cetak_data_btn.pack(side="left", padx=5)

            export_csv_btn = customtkinter.CTkButton(report_buttons_frame, text="Export ke CSV",
                                                    fg_color="#27AE60", hover_color="#229954",
                                                    command=export_data_to_csv, cursor="hand2")
            export_csv_btn.pack(side="left", padx=5)


    button_font = ("Arial", 12)
    button_fg_color = "#578FCA"
    button_text_color = "white"
    button_hover_color = "#3674B5"
    button_corner_radius = 8

    dashboard_btn = customtkinter.CTkButton(menu_buttons_container, text="Dashboard", font=button_font,
                                            fg_color=button_fg_color, text_color=button_text_color,
                                            hover_color=button_hover_color, corner_radius=button_corner_radius,
                                            command=lambda: show_page("dashboard"), cursor="hand2")
    dashboard_btn.pack(pady=(15, 10), padx=10, fill="x")

    validasi_data_btn = customtkinter.CTkButton(menu_buttons_container, text="Validasi Data", font=button_font,
                                                fg_color=button_fg_color, text_color=button_text_color,
                                                hover_color=button_hover_color, corner_radius=button_corner_radius,
                                                command=lambda: show_page("validasi_data"), cursor="hand2")
    validasi_data_btn.pack(pady=10, padx=10, fill="x")

    laporan_btn = customtkinter.CTkButton(menu_buttons_container, text="Laporan", font=button_font,
                                            fg_color=button_fg_color, text_color=button_text_color,
                                            hover_color=button_hover_color, corner_radius=button_corner_radius,
                                            command=lambda: show_page("laporan"), cursor="hand2")
    laporan_btn.pack(pady=10, padx=10, fill="x")

    logout_btn = customtkinter.CTkButton(logout_button_container, text="Logout", font=button_font,
                                            fg_color="red", text_color="white", hover_color="#cc0000",
                                            corner_radius=button_corner_radius,
                                            command=logout, cursor="hand2")
    logout_btn.pack(padx=10, fill="x")

    show_page("dashboard")

# Blok ini hanya berjalan jika file ini dieksekusi langsung (untuk pengujian)
if __name__ == '__main__':
    # Pastikan database telah diinisialisasi
    database.create_tables() 
    
