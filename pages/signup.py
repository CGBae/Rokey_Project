import flet as ft
from db import create_user


def show_signup(page: ft.Page, show_login):
    page.clean()
    page.padding = 0
    page.bgcolor = "#f5f6fa"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    name_field = ft.TextField(
        label="이름",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.BADGE,
    )

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

    pw_check_field = ft.TextField(
        label="PW 확인",
        password=True,
        can_reveal_password=True,
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.LOCK,
    )

    phone_field = ft.TextField(
        label="전화번호",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PHONE,
    )

    result_text = ft.Text(
        value="",
        size=14,
        color=ft.Colors.RED_400,
    )

    def signup_click(e):
        name_value = (name_field.value or "").strip()
        id_value = (id_field.value or "").strip()
        pw_value = (pw_field.value or "").strip()
        pw_check_value = (pw_check_field.value or "").strip()
        phone_value = (phone_field.value or "").strip()

        if not name_value or not id_value or not pw_value or not pw_check_value or not phone_value:
            result_text.value = "모든 항목을 입력하세요."
            result_text.color = ft.Colors.RED_400
            page.update()
            return

        if pw_value != pw_check_value:
            result_text.value = "비밀번호가 일치하지 않습니다."
            result_text.color = ft.Colors.RED_400
            pw_field.value = ""
            pw_check_field.value = ""
            page.update()
            return

        success = create_user(id_value, pw_value)

        if success:
            result_text.value = "회원가입이 완료되었습니다."
            result_text.color = ft.Colors.GREEN_500
        else:
            result_text.value = "이미 존재하는 ID입니다."
            result_text.color = ft.Colors.RED_400

        page.update()

    signup_button = ft.ElevatedButton(
        "회원가입",
        width=320,
        height=50,
        on_click=signup_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    back_button = ft.OutlinedButton(
        "로그인으로 돌아가기",
        width=320,
        height=50,
        on_click=lambda e: show_login(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    signup_card = ft.Container(
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
                ft.Text("Sign Up", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "회원 정보를 입력하세요",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=25),
                name_field,
                id_field,
                pw_field,
                pw_check_field,
                phone_field,
                ft.Container(height=10),
                result_text,
                ft.Container(height=15),
                signup_button,
                ft.Container(height=10),
                back_button,
            ],
        ),
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=signup_card,
        )
    )
    page.update()