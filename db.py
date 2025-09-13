import sqlite3
import os
import sys

def get_db_path():
    if getattr(sys, 'frozen', False):
        # .exe distributivda ishlayapti
        base_path = sys._MEIPASS
    else:
        # Terminalda ishlayapti
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "finance.db")

def get_connection():
    return sqlite3.connect(get_db_path())

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 💰 Daromadlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        note TEXT
    )
    """)

    # 💸 Xarajatlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        note TEXT
    )
    """)

    # 👤 Shaxslar jadvali (kreditor/debitor)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS person (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        note TEXT
    )
    """)

    # 📥 Kreditor qarzlari (qarz olingan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kreditor_debt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        due_date TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES person(id)
    )
    """)

    # 💸 Kreditor to‘lovlari (qarz qaytarilgan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kreditor_payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES person(id)
    )
    """)

    # 📤 Debitor qarzlari (qarz berilgan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS debitor_debt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        due_date TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES person(id)
    )
    """)

    # 💵 Debitor to‘lovlari (qarz undirilgan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS debitor_payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES person(id)
    )
    """)

    conn.commit()
    conn.close()
