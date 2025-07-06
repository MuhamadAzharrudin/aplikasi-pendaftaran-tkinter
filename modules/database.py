import sqlite3
import hashlib

DATABASE_NAME = 'mahasiswa.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Ini akan membuat kursor mengembalikan baris sebagai objek mirip kamus
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
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
    return hashed_password == hash_password(user_password)

if __name__ == '__main__':
    create_tables()
    print("Database 'mahasiswa.db' dan tabel 'users' berhasil dibuat/dicek.")
    conn = get_db_connection()
    cursor = conn.cursor()