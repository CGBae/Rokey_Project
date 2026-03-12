
import flet as ft

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





# =========================

# 메인 앱

# =========================

def main(page: ft.Page):

    page.title = "예약 프로그램"

    page.window_width = 500

    page.window_height = 700

    page.padding = 0

    page.bgcolor = "#f5f6fa"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.scroll = ft.ScrollMode.AUTO



    def show_login():

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



    def show_signup():

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



    def show_admin(user_id):

        page.clean()

        page.padding = 20

        page.bgcolor = "#f5f6fa"



        header = ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Column(

                    spacing=4,

                    controls=[

                        ft.Text("관리자 페이지", size=30, weight=ft.FontWeight.BOLD),

                        ft.Text(

                            f"{user_id} 계정으로 로그인되었습니다.",

                            size=14,

                            color=ft.Colors.GREY_700,

                        ),

                    ],

                ),

                ft.OutlinedButton(

                    "로그아웃",

                    width=120,

                    height=45,

                    on_click=lambda e: show_login(),

                    style=ft.ButtonStyle(

                        shape=ft.RoundedRectangleBorder(radius=12),

                    ),

                ),

            ],

        )



        summary_row = ft.Row(

            spacing=16,

            wrap=True,

            controls=[

                ft.Container(

                    width=140,

                    padding=20,

                    border_radius=18,

                    bgcolor=ft.Colors.WHITE,

                    shadow=ft.BoxShadow(

                        spread_radius=1,

                        blur_radius=14,

                        color=ft.Colors.BLACK12,

                        offset=ft.Offset(0, 3),

                    ),

                    content=ft.Column(

                        spacing=8,

                        controls=[

                            ft.Text("오늘 예약", size=15, color=ft.Colors.GREY_700),

                            ft.Text("0", size=30, weight=ft.FontWeight.BOLD),

                        ],

                    ),

                ),

                ft.Container(

                    width=140,

                    padding=20,

                    border_radius=18,

                    bgcolor=ft.Colors.WHITE,

                    shadow=ft.BoxShadow(

                        spread_radius=1,

                        blur_radius=14,

                        color=ft.Colors.BLACK12,

                        offset=ft.Offset(0, 3),

                    ),

                    content=ft.Column(

                        spacing=8,

                        controls=[

                            ft.Text("대기 예약", size=15, color=ft.Colors.GREY_700),

                            ft.Text("0", size=30, weight=ft.FontWeight.BOLD),

                        ],

                    ),

                ),

                ft.Container(

                    width=140,

                    padding=20,

                    border_radius=18,

                    bgcolor=ft.Colors.WHITE,

                    shadow=ft.BoxShadow(

                        spread_radius=1,

                        blur_radius=14,

                        color=ft.Colors.BLACK12,

                        offset=ft.Offset(0, 3),

                    ),

                    content=ft.Column(

                        spacing=8,

                        controls=[

                            ft.Text("완료 예약", size=15, color=ft.Colors.GREY_700),

                            ft.Text("0", size=30, weight=ft.FontWeight.BOLD),

                        ],

                    ),

                ),

            ],

        )



        admin_card = ft.Container(

            expand=True,

            padding=24,

            border_radius=20,

            bgcolor=ft.Colors.WHITE,

            shadow=ft.BoxShadow(

                spread_radius=1,

                blur_radius=18,

                color=ft.Colors.BLACK12,

                offset=ft.Offset(0, 4),

            ),

            content=ft.Column(

                spacing=16,

                controls=[

                    ft.Text("예약 관리", size=26, weight=ft.FontWeight.BOLD),

                    ft.Text(

                        "여기에 예약 목록과 상태 변경 기능을 추가하면 됩니다.",

                        size=14,

                        color=ft.Colors.GREY_700,

                    ),

                ],

            ),

        )



        page.add(

            ft.Column(

                expand=True,

                spacing=20,

                controls=[header, summary_row, admin_card],

            )

        )

        page.update()



    def show_user(user_id):

        page.clean()

        page.padding = 20

        page.bgcolor = "#f5f6fa"



        name_field = ft.TextField(

            label="예약자명",

            width=260,

            height=55,

            border_radius=12,

        )



        phone_field = ft.TextField(

            label="연락처",

            width=260,

            height=55,

            border_radius=12,

        )



        service_dropdown = ft.Dropdown(

            label="서비스 선택",

            width=260,

            border_radius=12,

            options=[

                ft.dropdown.Option("헤어컷"),

                ft.dropdown.Option("펌"),

                ft.dropdown.Option("염색"),

                ft.dropdown.Option("클리닉"),

            ],

        )



        date_field = ft.TextField(

            label="예약 날짜",

            hint_text="예: 2026-03-15",

            width=260,

            height=55,

            border_radius=12,

        )



        time_field = ft.TextField(

            label="예약 시간",

            hint_text="예: 14:00",

            width=260,

            height=55,

            border_radius=12,

        )



        request_field = ft.TextField(

            label="요청사항",

            multiline=True,

            min_lines=4,

            max_lines=6,

            width=540,

            border_radius=12,

        )



        result_text = ft.Text(

            value="",

            size=14,

            color=ft.Colors.RED_400,

        )



        reservation_list = ft.Column(spacing=12, controls=[])



        def make_reservation_card(name, phone, service, date, time, request):

            return ft.Container(

                padding=18,

                border_radius=16,

                bgcolor=ft.Colors.WHITE,

                shadow=ft.BoxShadow(

                    spread_radius=1,

                    blur_radius=12,

                    color=ft.Colors.BLACK12,

                    offset=ft.Offset(0, 3),

                ),

                content=ft.Column(

                    spacing=8,

                    controls=[

                        ft.Row(

                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                            controls=[

                                ft.Text(

                                    f"{service}",

                                    size=18,

                                    weight=ft.FontWeight.BOLD,

                                ),

                                ft.Container(

                                    padding=10,

                                    border_radius=20,

                                    bgcolor="#EAF2FF",

                                    content=ft.Text(

                                        "예약 완료",

                                        color="#1E5EFF",

                                        size=12,

                                        weight=ft.FontWeight.W_600,

                                    ),

                                ),

                            ],

                        ),

                        ft.Text(f"예약자: {name}", size=14),

                        ft.Text(f"연락처: {phone}", size=14),

                        ft.Text(f"예약 일시: {date} {time}", size=14),

                        ft.Text(

                            f"요청사항: {request if request else '없음'}",

                            size=14,

                            color=ft.Colors.GREY_700,

                        ),

                    ],

                ),

            )



        def reserve_click(e):

            name_value = (name_field.value or "").strip()

            phone_value = (phone_field.value or "").strip()

            service_value = service_dropdown.value

            date_value = (date_field.value or "").strip()

            time_value = (time_field.value or "").strip()

            request_value = (request_field.value or "").strip()



            if not name_value or not phone_value or not service_value or not date_value or not time_value:

                result_text.value = "필수 항목을 모두 입력하세요."

                result_text.color = ft.Colors.RED_400

                page.update()

                return



            new_card = make_reservation_card(

                name_value,

                phone_value,

                service_value,

                date_value,

                time_value,

                request_value,

            )



            reservation_list.controls.insert(0, new_card)



            result_text.value = "예약이 등록되었습니다."

            result_text.color = ft.Colors.GREEN_500



            name_field.value = ""

            phone_field.value = ""

            service_dropdown.value = None

            date_field.value = ""

            time_field.value = ""

            request_field.value = ""



            page.update()



        header = ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Column(

                    spacing=4,

                    controls=[

                        ft.Text("예약자 페이지", size=30, weight=ft.FontWeight.BOLD),

                        ft.Text(

                            f"{user_id} 계정으로 로그인되었습니다.",

                            size=14,

                            color=ft.Colors.GREY_700,

                        ),

                    ],

                ),

                ft.OutlinedButton(

                    "로그아웃",

                    width=120,

                    height=45,

                    on_click=lambda e: show_login(),

                    style=ft.ButtonStyle(

                        shape=ft.RoundedRectangleBorder(radius=12),

                    ),

                ),

            ],

        )



        form_card = ft.Container(

            expand=True,

            padding=24,

            border_radius=20,

            bgcolor=ft.Colors.WHITE,

            shadow=ft.BoxShadow(

                spread_radius=1,

                blur_radius=18,

                color=ft.Colors.BLACK12,

                offset=ft.Offset(0, 4),

            ),

            content=ft.Column(

                spacing=16,

                controls=[

                    ft.Text("예약 신청", size=26, weight=ft.FontWeight.BOLD),

                    ft.Text(

                        "원하는 서비스와 날짜를 입력해 예약하세요.",

                        size=14,

                        color=ft.Colors.GREY_600,

                    ),

                    ft.Row(

                        wrap=True,

                        spacing=16,

                        run_spacing=16,

                        controls=[

                            name_field,

                            phone_field,

                            service_dropdown,

                            date_field,

                            time_field,

                        ],

                    ),

                    request_field,

                    result_text,

                    ft.ElevatedButton(

                        "예약하기",

                        width=540,

                        height=50,

                        on_click=reserve_click,

                        style=ft.ButtonStyle(

                            shape=ft.RoundedRectangleBorder(radius=12),

                        ),

                    ),

                ],

            ),

        )



        reservation_card = ft.Container(

            expand=True,

            padding=24,

            border_radius=20,

            bgcolor=ft.Colors.WHITE,

            shadow=ft.BoxShadow(

                spread_radius=1,

                blur_radius=18,

                color=ft.Colors.BLACK12,

                offset=ft.Offset(0, 4),

            ),

            content=ft.Column(

                spacing=16,

                controls=[

                    ft.Text("내 예약 목록", size=26, weight=ft.FontWeight.BOLD),

                    ft.Text(

                        "최근 예약이 위쪽에 표시됩니다.",

                        size=14,

                        color=ft.Colors.GREY_600,

                    ),

                    reservation_list,

                ],

            ),

        )



        page.add(

            ft.Column(

                expand=True,

                spacing=20,

                controls=[header, form_card, reservation_card],

            )

        )

        page.update()



    show_login()





ft.app(target=main)