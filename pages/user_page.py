import flet as ft


def user_view(page: ft.Page):
    page.title = "예약자 페이지"
    page.window_width = 900
    page.window_height = 700
    page.padding = 20
    page.bgcolor = "#f5f6fa"
    page.scroll = ft.ScrollMode.AUTO

    name_field = ft.TextField(
        label="예약자명",
        width=260,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
    )

    phone_field = ft.TextField(
        label="연락처",
        width=260,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.PHONE_OUTLINED,
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
        prefix_icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
    )

    time_field = ft.TextField(
        label="예약 시간",
        hint_text="예: 14:00",
        width=260,
        height=55,
        border_radius=12,
        prefix_icon=ft.Icons.ACCESS_TIME_OUTLINED,
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

    reservation_list = ft.Column(
        spacing=12,
        controls=[],
    )

    def go_to_login(e=None):
        from pages.login import login_view
        page.clean()
        page.add(login_view(page))
        page.update()

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
                                padding=ft.Padding(10, 4, 10, 4),
                                border_radius=20,
                                bgcolor=ft.Colors.BLUE_50,
                                content=ft.Text(
                                    "예약 완료",
                                    color=ft.Colors.BLUE_700,
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
        name_value = name_field.value.strip()
        phone_value = phone_field.value.strip()
        service_value = service_dropdown.value
        date_value = date_field.value.strip()
        time_value = time_field.value.strip()
        request_value = request_field.value.strip()

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

    reserve_button = ft.ElevatedButton(
        "예약하기",
        width=540,
        height=50,
        on_click=reserve_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    logout_button = ft.OutlinedButton(
        "로그아웃",
        width=140,
        height=45,
        on_click=go_to_login,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
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
                reserve_button,
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

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("예약자 페이지", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "서비스 예약과 예약 내역 확인이 가능합니다.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                ],
            ),
            logout_button,
        ],
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                header,
                form_card,
                reservation_card,
            ],
        ),
    )