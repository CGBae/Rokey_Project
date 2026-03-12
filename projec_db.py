import flet as ft
import sqlite3

# DB 생성 및 연결
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()


def main(page: ft.Page):

    login_id = ft.TextField(label="ID")
    login_pw = ft.TextField(label="Password", password=True)

    signup_id = ft.TextField(label="New ID")
    signup_pw = ft.TextField(label="New Password", password=True)

    message = ft.Text()

    # 로그인 함수
    def login(e):
        cursor.execute(
            "SELECT * FROM users WHERE id=? AND password=?",
            (login_id.value, login_pw.value),
        )
        result = cursor.fetchone()

        if result:
            message.value = "로그인 성공!"
        else:
            message.value = "ID 또는 비밀번호가 틀립니다."
        page.update()

    # 회원가입 함수
    def signup(e):
        try:
            cursor.execute(
                "INSERT INTO users VALUES (?, ?)",
                (signup_id.value, signup_pw.value),
            )
            conn.commit()
            message.value = "회원가입 성공!"
        except:
            message.value = "이미 존재하는 ID입니다."
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("로그인", size=25),
                login_id,
                login_pw,
                ft.ElevatedButton("Login", on_click=login),
                ft.Divider(),
                ft.Text("회원가입", size=25),
                signup_id,
                signup_pw,
                ft.ElevatedButton("Sign Up", on_click=signup),
                message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(target=main)