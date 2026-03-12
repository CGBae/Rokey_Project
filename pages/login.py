import flet as ft
from db import login_user


def show_login(page: ft.Page, show_signup, show_admin, show_user):
    page.clean()
    page.padding = 0
    page.bgcolor = "#f5f6fa"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    id_field = ft.TextField(
        label="ID",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PERSON,
    )

    pw_field = ft.TextField(
        label="PW",
        password=True,
        can_reveal_password=True,
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.LOCK,
    )

    result_text = ft.Text(
        value="",
        size=14,
        color=ft.Colors.RED_400,
    )

    def login_click(e):
        user_id = (id_field.value or "").strip()
        user_pw = (pw_field.value or "").strip()

        if not user_id or not user_pw:
            result_text.value = "아이디와 비밀번호를 모두 입력하세요."
            result_text.color = ft.Colors.RED_400
            page.update()
            return

        result = login_user(user_id, user_pw)

        if result is not None:
            if user_id == "admin":
                show_admin(user_id)
            else:
                show_user(user_id)
        else:
            result_text.value = "ID 또는 비밀번호가 올바르지 않습니다."
            result_text.color = ft.Colors.RED_400
            page.update()

    login_button = ft.ElevatedButton(
        "Login",
        width=320,
        height=50,
        on_click=login_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    signup_button = ft.OutlinedButton(
        "Sign Up",
        width=320,
        height=50,
        on_click=lambda e: show_signup(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    login_card = ft.Container(
        width=380,
        padding=30,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=18,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            controls=[
                ft.Text("Login", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "예약 시스템에 로그인하세요",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=25),
                id_field,
                pw_field,
                ft.Container(height=10),
                result_text,
                ft.Container(height=15),
                login_button,
                ft.Container(height=10),
                signup_button,
            ],
        ),
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=login_card,
        )
    )
    page.update()