import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "reservation.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# 회원 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    password TEXT
)
""")

# 기본 관리자 계정
cursor.execute(
    "INSERT OR IGNORE INTO users (id, password) VALUES (?, ?)",
    ("admin", "admin")
)

# 예약 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    service TEXT NOT NULL,
    approved INTEGER DEFAULT 0
)
""")

conn.commit()


# -------------------------
# 회원 관련
# -------------------------
def create_user(user_id, password):
    try:
        cursor.execute(
            "INSERT INTO users (id, password) VALUES (?, ?)",
            (user_id, password),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(user_id, password):
    cursor.execute(
        "SELECT id, password FROM users WHERE id=? AND password=?",
        (user_id, password),
    )
    return cursor.fetchone()


# -------------------------
# 예약 관련
# -------------------------
def add_reservation(user_id, name, phone, date, time, service):
    cursor.execute(
        """
        INSERT INTO reservations (user_id, name, phone, date, time, service)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, name, phone, date, time, service)
    )
    conn.commit()


def get_reservations():
    cursor.execute("SELECT * FROM reservations ORDER BY id DESC")
    return cursor.fetchall()


def get_user_reservations(user_id):
    cursor.execute(
        "SELECT * FROM reservations WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )
    return cursor.fetchall()


def approve_reservation(reservation_id, current_user):
    if current_user != "admin":
        return False

    cursor.execute(
        "UPDATE reservations SET approved = 1 WHERE id = ?",
        (reservation_id,)
    )
    conn.commit()
    return True