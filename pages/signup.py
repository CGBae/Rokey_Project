import flet as ft


def signup_view(page: ft.Page):
    page.title = "회원가입"
    page.window_width = 500
    page.window_height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = "#f5f6fa"

    name_field = ft.TextField(
        label="이름",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.BADGE_OUTLINED,
    )

    id_field = ft.TextField(
        label="ID",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
    )

    pw_field = ft.TextField(
        label="PW",
        password=True,
        can_reveal_password=True,
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
    )

    pw_check_field = ft.TextField(
        label="PW 확인",
        password=True,
        can_reveal_password=True,
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.LOCK_RESET_OUTLINED,
    )

    phone_field = ft.TextField(
        label="전화번호",
        width=320,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PHONE_OUTLINED,
    )

    result_text = ft.Text(
        value="",
        size=14,
        color=ft.Colors.RED_400,
    )

    def go_to_login(e=None):
        from pages.login import login_view
        page.clean()
        page.add(login_view(page))
        page.update()

    def signup_click(e):
        name_value = name_field.value.strip()
        id_value = id_field.value.strip()
        pw_value = pw_field.value.strip()
        pw_check_value = pw_check_field.value.strip()
        phone_value = phone_field.value.strip()

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

        # 나중에 여기서 실제 회원가입 함수 연결
        # 예: result = register_user(name_value, id_value, pw_value, phone_value)

        result_text.value = "회원가입이 완료되었습니다."
        result_text.color = ft.Colors.GREEN_500
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
        on_click=go_to_login,
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

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=signup_card,
    )