import sqlite3
from datetime import date

DB_PATH = "hbitlogs.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS hbits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hbit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (hbit_id) REFERENCES hbits(id)
            )
        ''')
        conn.commit()

def add_hbit(name):
    today = date.today().isoformat()
    with get_connection() as conn:
        try:
            conn.execute("INSERT INTO hbits (name, created) VALUES (?, ?)", (name, today))
            print(f"✅ Added habit: {name}")
        except sqlite3.IntegrityError:
            print(f"⚠️ Habit already exists: {name}")

def log_hbit(name):
    today = date.today().isoformat()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM hbits WHERE name = ?", (name,))
        row = c.fetchone()
        if not row:
            print(f"⚠️ Habit not found: {name}")
            return
        hbit_id = row[0]
        c.execute("SELECT id FROM logs WHERE hbit_id = ? AND date = ?", (hbit_id, today))
        if c.fetchone():
            print(f"⏱️ Already logged today for: {name}")
            return
        c.execute("INSERT INTO logs (hbit_id, date) VALUES (?, ?)", (hbit_id, today))
        conn.commit()
        print(f"🗓️ Logged {name} for today!")

def list_hbits():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name, created FROM hbits ORDER BY name")
        rows = c.fetchall()
        if not rows:
            print("📭 No habits yet. Add one with: add <name>")
        else:
            print("📋 Tracked habits:")
            for name, created in rows:
                print(f" - {name} (since {created})")

def show_stats(name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM hbits WHERE name = ?", (name,))
        row = c.fetchone()
        if not row:
            print(f"⚠️ Habit not found: {name}")
            return
        hbit_id = row[0]
        c.execute("SELECT COUNT(*), MAX(date) FROM logs WHERE hbit_id = ?", (hbit_id,))
        total, last = c.fetchone()
        print(f"📊 Stats for '{name}':")
        print(f" - Total logged: {total} times")
        print(f" - Last entry : {last if last else 'Never'}")

def remove_hbit(name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM hbits WHERE name = ?", (name,))
        row = c.fetchone()
        if not row:
            print(f"⚠️ Habit not found: {name}")
            return
        hbit_id = row[0]
        # Delete logs first to avoid foreign key constraint
        c.execute("DELETE FROM logs WHERE hbit_id = ?", (hbit_id,))
        c.execute("DELETE FROM hbits WHERE id = ?", (hbit_id,))
        conn.commit()
        print(f"❌ Removed habit: {name}")

