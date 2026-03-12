import sqlite3

conn = sqlite3.connect("reservation.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    service TEXT NOT NULL,
    approved INTEGER DEFAULT 0
)
""")

conn.commit()

def add_reservation(name, phone, date, time, service):      # 예약 데이터
    cursor.execute(
        """
        INSERT INTO reservations (name, phone, date, time, service)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, phone, date, time, service)
    )
    conn.commit()
    
def get_reservations():     # 예약 목록 조회
    cursor.execute("SELECT * FROM reservations")
    return cursor.fetchall()

def approve_reservation(reservation_id, current_user):  # 승인 코드
    # reservation_id = 예약번호
    if current_user != "admin":
        print("관리자만 승인 가능")
        return

    cursor.execute(
        "UPDATE reservations SET approved = 1 WHERE id = ?",
        (reservation_id,)
    )
    conn.commit()

def approve_sign():     # 승인 여부 표시
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()

    for r in rows:
        status = "승인" if r[6] == 1 else "대기"
        print(r[1], r[2], r[3], r[4], r[5], status)
        # r = [r[1]=name, r[2]=phone, ... r[6]=status]
        # r[0] = 예약번호



