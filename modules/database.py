import sqlite3
import hashlib
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

DATABASE_NAME = 'mahasiswa.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            level TEXT DEFAULT 'siswa'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pendaftar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nama_lengkap TEXT NOT NULL,
            tempat_lahir TEXT NOT NULL,
            tanggal_lahir TEXT NOT NULL,
            asal_sekolah TEXT NOT NULL,
            nomor_hp TEXT NOT NULL,
            nilai_ujian_sekolah REAL,
            nilai_ujian_nasional REAL,
            status_pendaftaran TEXT DEFAULT 'Belum Mendaftar',
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')
    
    # --- START Penambahan Kode untuk jenis_kelamin ---
    # Cek apakah kolom jenis_kelamin sudah ada di tabel pendaftar
    cursor.execute("PRAGMA table_info(pendaftar)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'jenis_kelamin' not in columns:
        cursor.execute("ALTER TABLE pendaftar ADD COLUMN jenis_kelamin TEXT")
    # --- END Penambahan Kode untuk jenis_kelamin ---

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
    return hashed_password == hash_password(user_password)

def get_user_by_username(username):
    """Mengambil data user berdasarkan username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(email, username, password, level='siswa'):
    """Mendaftarkan user baru."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_pass = hash_password(password)
        cursor.execute("INSERT INTO users (email, username, password, level) VALUES (?, ?, ?, ?)",
                       (email, username, hashed_pass, level))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def save_pendaftaran_data(username, data):
    """
    Menyimpan atau memperbarui data pendaftaran siswa.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    user_exists = get_user_by_username(username)
    if not user_exists:
        conn.close()
        return False, "Error: User tidak ditemukan."

    cursor.execute("SELECT * FROM pendaftar WHERE username = ?", (username,))
    existing_data = cursor.fetchone()

    if existing_data:
        # --- START Penambahan Kode untuk jenis_kelamin ---
        cursor.execute('''
            UPDATE pendaftar SET
                nama_lengkap = ?,
                jenis_kelamin = ?, 
                tempat_lahir = ?,
                tanggal_lahir = ?,
                asal_sekolah = ?,
                nomor_hp = ?,
                nilai_ujian_sekolah = ?,
                nilai_ujian_nasional = ?,
                status_pendaftaran = 'Menunggu Verifikasi'
            WHERE username = ?
        ''', (data['nama_lengkap'], data['jenis_kelamin'], data['tempat_lahir'], data['tanggal_lahir'],
              data['asal_sekolah'], data['nomor_hp'], data['nilai_ujian_sekolah'],
              data['nilai_ujian_nasional'], username))
        # --- END Penambahan Kode untuk jenis_kelamin ---
        message = "Data pendaftaran berhasil diperbarui."
    else:
        # --- START Penambahan Kode untuk jenis_kelamin ---
        cursor.execute('''
            INSERT INTO pendaftar (
                username, nama_lengkap, jenis_kelamin, tempat_lahir, tanggal_lahir,
                asal_sekolah, nomor_hp, nilai_ujian_sekolah, nilai_ujian_nasional,
                status_pendaftaran
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, data['nama_lengkap'], data['jenis_kelamin'], data['tempat_lahir'], data['tanggal_lahir'],
              data['asal_sekolah'], data['nomor_hp'], data['nilai_ujian_sekolah'],
              data['nilai_ujian_nasional'], 'Menunggu Verifikasi'))
        # --- END Penambahan Kode untuk jenis_kelamin ---
        message = "Data pendaftaran berhasil disimpan."
    
    conn.commit()
    conn.close()
    return True, message

def get_pendaftaran_data(username):
    """Mengambil data pendaftaran siswa berdasarkan username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # --- START Penambahan Kode untuk jenis_kelamin ---
    cursor.execute("SELECT nama_lengkap, jenis_kelamin, tempat_lahir, tanggal_lahir, asal_sekolah, nomor_hp, nilai_ujian_sekolah, nilai_ujian_nasional, status_pendaftaran FROM pendaftar WHERE username = ?", (username,))
    # --- END Penambahan Kode untuk jenis_kelamin ---
    row = cursor.fetchone()
    conn.close()

    if row:
        # --- START Penambahan Kode untuk jenis_kelamin ---
        return {
            "nama_lengkap": row["nama_lengkap"],
            "jenis_kelamin": row["jenis_kelamin"], 
            "tempat_lahir": row["tempat_lahir"],
            "tanggal_lahir": row["tanggal_lahir"],
            "asal_sekolah": row["asal_sekolah"],
            "nomor_hp": row["nomor_hp"],
            "nilai_ujian_sekolah": row["nilai_ujian_sekolah"],
            "nilai_ujian_nasional": row["nilai_ujian_nasional"],
            "status_pendaftaran": row["status_pendaftaran"]
        }
        # --- END Penambahan Kode untuk jenis_kelamin ---
    return None

def generate_bukti_pendaftaran_pdf(filepath, username, pendaftaran_data):
    """
    Menghasilkan file PDF bukti pendaftaran dengan kop surat dan tabel detail.
    Args:
        filepath (str): Path lengkap untuk menyimpan file PDF.
        username (str): Username siswa.
        pendaftaran_data (dict): Dictionary berisi data pendaftaran siswa.
    Returns:
        bool: True jika berhasil, False jika gagal.
    """
    try:
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Membuat gaya paragraf custom untuk kop surat yang rata tengah
        center_style = ParagraphStyle(
            name='CenterStyle',
            parent=styles['Normal'],
            alignment=1,  # 0=left, 1=center, 2=right, 4=justify
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Gaya untuk header kop surat (ukuran lebih besar)
        header_kop_style = ParagraphStyle(
            name='HeaderKopStyle',
            parent=styles['h1'],
            alignment=1,
            fontSize=16,
            leading=18, # Jarak antar baris
            spaceAfter=0,
            spaceBefore=0,
        )
        
        # Gaya untuk alamat kop surat
        address_kop_style = ParagraphStyle(
            name='AddressKopStyle',
            parent=styles['Normal'],
            alignment=1,
            fontSize=10,
            leading=12,
            spaceAfter=0,
            spaceBefore=0,
        )

        # --- Kop Surat / Kop Sekolah ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        logo_path = os.path.join(project_root, "assets", "images", "logo_sekolah.png")

        if os.path.exists(logo_path):
            img = Image(logo_path, width=1.0*inch, height=1.0*inch)
            
            # Teks kop surat yang sudah diatur ke tengah
            kop_text = Paragraph("<font size=14><b>CALON SISWA BARU</b></font><br/>"
                                 "<font size=12><b>SMA NEGERI 1 AIKMEL</b></font><br/>"
                                 "<font size=10>Jl. Pendidikan No. 88, Kec. Aikmel, Kab. Lombok Timur</font>", center_style)
            
            # Data untuk tabel kop
            # Untuk memusatkan tabel secara keseluruhan, kita bisa menempatkan logo dan teks dalam satu sel
            # dan mengatur lebar kolom agar logo tidak mendominasi, atau menempatkannya dalam dua kolom
            # dan menyesuaikan align masing-masing.
            # Untuk kop surat dengan logo di kiri dan teks di tengah relatif terhadap lebar kop secara keseluruhan,
            # kita bisa menggunakan satu sel besar untuk teks yang diatur tengah.
            
            # Opsi 1: Logo di kiri, teks di tengah (seperti sebelumnya, tapi lebih baik)
            kop_data = [
                [img, kop_text]
            ]
            
            # Gunakan lebar kolom yang lebih fleksibel
            # A4[0] adalah lebar halaman, kurangi margin default (2*inch)
            kop_table = Table(kop_data, colWidths=[1.2*inch, A4[0] - 2*inch - 1.2*inch]) # Kolom kedua mengambil sisa
            
            kop_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (0,0), (0,-1), 'LEFT'), # Logo di kiri selnya
                ('ALIGN', (1,0), (-1,-1), 'CENTER'), # Teks kop surat di tengah selnya
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ]))
            
            kop_table.hAlign = 'CENTER' # <--- PENTING: Untuk memusatkan tabel kop surat itu sendiri
            story.append(kop_table)

        else:
            # Jika tidak ada logo, buat kop surat tanpa logo
            story.append(Paragraph("<font size=16><b>BUKTI PENDAFTARAN CALON PESERTA DIDIK BARU</b></font>", header_kop_style))
            story.append(Paragraph("<font size=14><b>SMA NEGERI 1 AIKMEL</b></font>", header_kop_style))
            story.append(Paragraph("Jl. Pendidikan No. 88, Kec. Aikmel, Kab. Lombok Timur", address_kop_style))
        
        story.append(Spacer(1, 0.2 * inch))
        # Garis pembatas, kita juga ingin ini di tengah
        hr_style = styles['Normal']
        hr_style.alignment = 1 # Center the line (though line doesn't align itself like text)
        story.append(Paragraph("<hr/>", hr_style))  # Garis horizontal
        story.append(Spacer(1, 0.3 * inch))


        # --- Informasi Siswa dan Status ---
        story.append(Paragraph(f"<b>Nama Siswa:</b> {username}", styles['Normal']))
        
        # Tambahkan status LULUS di bawah nama siswa
        if pendaftaran_data.get("status_pendaftaran") == "Lulus":
            story.append(Paragraph(f"<b>Status:</b> <font color='green'>LULUS</font>", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Status:</b> {pendaftaran_data.get('status_pendaftaran', 'Belum Mendaftar')}", styles['Normal']))

        story.append(Spacer(1, 0.1 * inch))

        # --- Data Pendaftaran dalam Tabel ---
        # --- START Penambahan Kode untuk jenis_kelamin ---
        data = [
            ["NAMA LENGKAP", pendaftaran_data.get("nama_lengkap", "Belum Diisi")],
            ["JENIS KELAMIN", pendaftaran_data.get("jenis_kelamin", "Belum Diisi")], # Tambahkan ini
            ["TEMPAT, TANGGAL LAHIR", f"{pendaftaran_data.get('tempat_lahir', 'Belum Diisi')}, {pendaftaran_data.get('tanggal_lahir', 'Belum Diisi')}"],
            ["ASAL SEKOLAH", pendaftaran_data.get("asal_sekolah", "Belum Diisi")],
            ["NOMOR HP", pendaftaran_data.get("nomor_hp", "Belum Diisi")],
            ["NILAI UJIAN SEKOLAH", pendaftaran_data.get("nilai_ujian_sekolah", "Belum Diisi")],
            ["NILAI UJIAN NASIONAL", pendaftaran_data.get("nilai_ujian_nasional", "Belum Diisi")]
        ]
        # --- END Penambahan Kode untuk jenis_kelamin ---

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#ADC4F4")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ])
        
        table_data = []
        for row_data in data:
            table_data.append([Paragraph(str(cell), styles['Normal']) for cell in row_data])

        table = Table(table_data, colWidths=[2.5*inch, None])
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 0.5 * inch))

        # --- Catatan Kaki ---
        footer_text = f"Dokumen ini dicetak otomatis pada tanggal {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}."
        # Catatan kaki juga bisa di tengah
        footer_style = styles['Italic']
        footer_style.alignment = 1
        story.append(Paragraph(footer_text, footer_style))

        doc.build(story)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
    
def get_total_pendaftar():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pendaftar")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_pendaftar_by_status(status):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row # Agar bisa akses kolom by nama
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pendaftar WHERE status_pendaftaran = ?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows] # Mengembalikan list of dictionaries

def get_all_pendaftar_data():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pendaftar")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == '__main__':
    create_tables()
    print("Database 'mahasiswa.db' dan tabel 'users' & 'pendaftar' berhasil disimpan.")