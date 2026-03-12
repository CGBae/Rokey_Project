import sqlite3
from pathlib import Path

# =========================
# DB 설정
# =========================
DB_PATH = Path(__file__).resolve().parent / "users.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# 기본 관리자 계정 추가
cursor.execute(
    "INSERT OR IGNORE INTO users (id, password) VALUES (?, ?)",
    ("admin", "admin")
)
conn.commit()


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