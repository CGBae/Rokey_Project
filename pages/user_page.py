import flet as ft
from datetime import datetime, timedelta, time
from db import add_reservation, get_user_reservations


def show_user(page: ft.Page, show_login, user_id):
    page.clean()
    page.padding = 20
    page.bgcolor = "#f5f6fa"

    name_field = ft.TextField(
        label="예약자명",
        width=260,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PERSON,
    )

    phone_field = ft.TextField(
        label="연락처",
        hint_text="숫자만 입력",
        width=260,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PHONE,
        keyboard_type=ft.KeyboardType.PHONE,
        max_length=13,
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
        hint_text="날짜 선택 버튼 클릭",
        width=260,
        height=55,
        border_radius=12,
        read_only=True,
        prefix_icon=ft.Icons.CALENDAR_MONTH,
    )

    time_field = ft.TextField(
        label="예약 시간",
        hint_text="시간 선택 버튼 클릭",
        width=260,
        height=55,
        border_radius=12,
        read_only=True,
        prefix_icon=ft.Icons.ACCESS_TIME,
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

    def format_phone_number(value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())[:11]

        if len(digits) < 4:
            return digits
        if len(digits) < 8:
            return f"{digits[:3]}-{digits[3:]}"
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"

    def phone_change(e):
        formatted = format_phone_number(phone_field.value or "")
        if phone_field.value != formatted:
            phone_field.value = formatted
            page.update()

    phone_field.on_change = phone_change

    def on_date_change(e):
        if date_picker.value:
            date_field.value = date_picker.value.strftime("%Y-%m-%d")
            page.update()

    def on_time_change(e):
        if time_picker.value:
            selected_time = time_picker.value
            time_field.value = selected_time.strftime("%H:%M")
            page.update()

    today = datetime.now()

    date_picker = ft.DatePicker(
        first_date=today,
        last_date=today + timedelta(days=90),
        help_text="예약 날짜 선택",
        confirm_text="확인",
        cancel_text="취소",
        on_change=on_date_change,
    )

    time_picker = ft.TimePicker(
        value=time(hour=10, minute=0),
        help_text="예약 시간 선택",
        confirm_text="확인",
        cancel_text="취소",
        on_change=on_time_change,
        hour_format=ft.TimePickerHourFormat.H24,
    )

    def open_date_picker(e):
        page.show_dialog(date_picker)

    def open_time_picker(e):
        page.show_dialog(time_picker)

    def make_reservation_card(reservation):
        reservation_id = reservation[0]
        name = reservation[2]
        phone = reservation[3]
        date = reservation[4]
        time_value = reservation[5]
        service = reservation[6]
        approved = reservation[7]

        status_text = "승인" if approved == 1 else "대기"
        status_bg = "#E8F5E9" if approved == 1 else "#FFF3E0"
        status_color = "#2E7D32" if approved == 1 else "#EF6C00"

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
                                bgcolor=status_bg,
                                content=ft.Text(
                                    status_text,
                                    color=status_color,
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(f"예약번호: {reservation_id}", size=13),
                    ft.Text(f"예약자: {name}", size=14),
                    ft.Text(f"연락처: {phone}", size=14),
                    ft.Text(f"예약 일시: {date} {time_value}", size=14),
                ],
            ),
        )

    def refresh_reservations():
        reservation_list.controls.clear()
        rows = get_user_reservations(user_id)

        for r in rows:
            reservation_list.controls.append(make_reservation_card(r))

        page.update()

    def reserve_click(e):
        name_value = (name_field.value or "").strip()
        phone_value = (phone_field.value or "").strip()
        service_value = service_dropdown.value
        date_value = (date_field.value or "").strip()
        time_value = (time_field.value or "").strip()

        if not name_value or not phone_value or not service_value or not date_value or not time_value:
            result_text.value = "필수 항목을 모두 입력하세요."
            result_text.color = ft.Colors.RED_400
            page.update()
            return

        add_reservation(
            user_id,
            name_value,
            phone_value,
            date_value,
            time_value,
            service_value,
        )

        result_text.value = "예약이 등록되었습니다."
        result_text.color = ft.Colors.GREEN_500

        name_field.value = ""
        phone_field.value = ""
        service_dropdown.value = None
        date_field.value = ""
        time_field.value = ""
        request_field.value = ""

        refresh_reservations()

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
                    ],
                ),
                ft.Row(
                    wrap=True,
                    spacing=16,
                    run_spacing=16,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                date_field,
                                ft.IconButton(
                                    icon=ft.Icons.CALENDAR_MONTH,
                                    tooltip="날짜 선택",
                                    on_click=open_date_picker,
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=8,
                            controls=[
                                time_field,
                                ft.IconButton(
                                    icon=ft.Icons.ACCESS_TIME,
                                    tooltip="시간 선택",
                                    on_click=open_time_picker,
                                ),
                            ],
                        ),
                    ],
                ),
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

    refresh_reservations()