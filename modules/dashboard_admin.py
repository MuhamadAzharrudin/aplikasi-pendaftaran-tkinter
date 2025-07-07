# modules/dashboard_admin.py

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import customtkinter
import os 

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
            title_label = customtkinter.CTkLabel(content_frame, text="Selamat Datang di Dashboard Admin!",
                                                 font=("Helvetica", 24, "bold"), text_color="#093FB4")
            title_label.pack(pady=20)
            
            customtkinter.CTkLabel(content_frame, text="Anda dapat mengelola data pendaftar dan melihat laporan.",
                                   font=("Arial", 16), text_color="#333333").pack(pady=10)
            customtkinter.CTkLabel(content_frame, text="Gunakan menu di samping untuk navigasi.",
                                   font=("Arial", 12), text_color="#666666").pack(pady=5)

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

            customtkinter.CTkLabel(content_frame, text="Halaman ini akan menampilkan laporan pendaftaran siswa.",
                                   font=("Arial", 16), text_color="#333333").pack(pady=10)
            customtkinter.CTkLabel(content_frame, text="Fitur filter dan generate PDF/Excel akan ditambahkan di sini.",
                                   font=("Arial", 12), text_color="#666666").pack(pady=5)
            
            generate_report_btn = customtkinter.CTkButton(content_frame, text="Generate Laporan (PDF)",
                                                           fg_color="#093FB4", hover_color="#07308D",
                                                           command=lambda: messagebox.showinfo("Info", "Fitur generate laporan akan datang!"),
                                                           cursor="hand2")
            generate_report_btn.pack(pady=20)

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
