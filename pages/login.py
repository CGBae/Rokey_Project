import flet as ft


def login_view(page: ft.Page):
    page.title = "예약 프로그램"
    page.window_width = 500
    page.window_height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = "#f5f6fa"

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

    result_text = ft.Text(
        value="",
        size=14,
        color=ft.Colors.RED_400,
    )

    def check_login(user_id, user_pw):
        if user_id == "admin" and user_pw == "admin":
            return True
        return False

    def login_click(e):
        user_id = id_field.value.strip()
        user_pw = pw_field.value.strip()

        if not user_id or not user_pw:
            result_text.value = "아이디와 비밀번호를 모두 입력하세요."
            result_text.color = ft.Colors.RED_400
            page.update()
            return

        is_success = check_login(user_id, user_pw)

        if is_success:
            result_text.value = "로그인 성공!"
            result_text.color = ft.Colors.GREEN_500
        else:
            result_text.value = "아이디 또는 비밀번호가 올바르지 않습니다."
            result_text.color = ft.Colors.RED_400

        page.update()

    def signup_click(e):
        from pages.signup import signup_view
        page.clean()
        page.add(signup_view(page))
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
        on_click=signup_click,
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

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=login_card,
    )