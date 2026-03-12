import flet as ft


def show_user(page: ft.Page, show_login, user_id):
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