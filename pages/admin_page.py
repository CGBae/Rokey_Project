import flet as ft


def admin_view(page: ft.Page):
    page.title = "관리자 페이지"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    page.bgcolor = "#f5f6fa"
    page.scroll = ft.ScrollMode.AUTO

    search_field = ft.TextField(
        label="예약자 검색",
        hint_text="이름 또는 서비스 검색",
        width=300,
        height=50,
        border_radius=12,
        prefix_icon=ft.Icons.SEARCH,
    )

    result_text = ft.Text(
        value="",
        size=14,
        color=ft.Colors.BLUE_600,
    )

    reservation_column = ft.Column(spacing=12)

    sample_data = [
        {
            "name": "김철수",
            "phone": "010-1111-2222",
            "service": "헤어컷",
            "date": "2026-03-12",
            "time": "10:00",
            "request": "짧게 정리",
            "status": "대기",
        },
        {
            "name": "이영희",
            "phone": "010-3333-4444",
            "service": "펌",
            "date": "2026-03-12",
            "time": "13:00",
            "request": "굵은 웨이브",
            "status": "확정",
        },
        {
            "name": "박민수",
            "phone": "010-5555-6666",
            "service": "염색",
            "date": "2026-03-12",
            "time": "15:30",
            "request": "밝은 갈색",
            "status": "완료",
        },
    ]

    def go_to_login(e=None):
        from pages.login import login_view
        page.clean()
        page.add(login_view(page))
        page.update()

    def status_chip(status: str):
        if status == "대기":
            bg = ft.Colors.ORANGE_50
            fg = ft.Colors.ORANGE_700
        elif status == "확정":
            bg = ft.Colors.BLUE_50
            fg = ft.Colors.BLUE_700
        elif status == "완료":
            bg = ft.Colors.GREEN_50
            fg = ft.Colors.GREEN_700
        else:
            bg = ft.Colors.GREY_200
            fg = ft.Colors.GREY_700

        return ft.Container(
            padding=ft.Padding(10, 5, 10, 5),
            border_radius=20,
            bgcolor=bg,
            content=ft.Text(
                status,
                size=12,
                color=fg,
                weight=ft.FontWeight.W_600,
            ),
        )

    def create_reservation_card(item):
        status_text = ft.Text(item["status"])

        def set_waiting(e):
            item["status"] = "대기"
            refresh_list()
            result_text.value = f'{item["name"]}님의 예약 상태가 대기로 변경되었습니다.'
            page.update()

        def set_confirmed(e):
            item["status"] = "확정"
            refresh_list()
            result_text.value = f'{item["name"]}님의 예약 상태가 확정으로 변경되었습니다.'
            page.update()

        def set_done(e):
            item["status"] = "완료"
            refresh_list()
            result_text.value = f'{item["name"]}님의 예약 상태가 완료로 변경되었습니다.'
            page.update()

        return ft.Container(
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
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f'{item["name"]} / {item["service"]}',
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            status_chip(item["status"]),
                        ],
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"sm": 6, "md": 4},
                                content=ft.Text(f'연락처: {item["phone"]}', size=14),
                            ),
                            ft.Container(
                                col={"sm": 6, "md": 4},
                                content=ft.Text(
                                    f'예약 일시: {item["date"]} {item["time"]}',
                                    size=14,
                                ),
                            ),
                            ft.Container(
                                col={"sm": 12, "md": 4},
                                content=ft.Text(
                                    f'요청사항: {item["request"] if item["request"] else "없음"}',
                                    size=14,
                                ),
                            ),
                        ]
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        controls=[
                            ft.OutlinedButton(
                                "대기",
                                on_click=set_waiting,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.ElevatedButton(
                                "확정",
                                on_click=set_confirmed,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.FilledButton(
                                "완료",
                                on_click=set_done,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def refresh_list(keyword: str = ""):
        reservation_column.controls.clear()

        filtered = sample_data
        if keyword:
            keyword = keyword.strip().lower()
            filtered = [
                item
                for item in sample_data
                if keyword in item["name"].lower() or keyword in item["service"].lower()
            ]

        if not filtered:
            reservation_column.controls.append(
                ft.Container(
                    padding=20,
                    border_radius=16,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Text("검색 결과가 없습니다.", size=16),
                )
            )
        else:
            for item in filtered:
                reservation_column.controls.append(create_reservation_card(item))

        page.update()

    def search_click(e):
        refresh_list(search_field.value)

    summary_card_1 = ft.Container(
        width=250,
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
                ft.Text("오늘 예약", size=16, color=ft.Colors.GREY_700),
                ft.Text(str(len(sample_data)), size=30, weight=ft.FontWeight.BOLD),
            ],
        ),
    )

    summary_card_2 = ft.Container(
        width=250,
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
                ft.Text("대기 예약", size=16, color=ft.Colors.GREY_700),
                ft.Text(
                    str(len([x for x in sample_data if x["status"] == "대기"])),
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        ),
    )

    summary_card_3 = ft.Container(
        width=250,
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
                ft.Text("완료 예약", size=16, color=ft.Colors.GREY_700),
                ft.Text(
                    str(len([x for x in sample_data if x["status"] == "완료"])),
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
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
                    ft.Text("관리자 페이지", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "예약 현황을 확인하고 상태를 관리할 수 있습니다.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                ],
            ),
            ft.OutlinedButton(
                "로그아웃",
                width=140,
                height=45,
                on_click=go_to_login,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
        ],
    )

    search_bar = ft.Row(
        wrap=True,
        spacing=10,
        controls=[
            search_field,
            ft.ElevatedButton(
                "검색",
                height=50,
                on_click=search_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
            ft.OutlinedButton(
                "전체보기",
                height=50,
                on_click=lambda e: refresh_list(""),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
        ],
    )

    summary_section = ft.Row(
        spacing=16,
        wrap=True,
        controls=[
            summary_card_1,
            summary_card_2,
            summary_card_3,
        ],
    )

    reservation_section = ft.Container(
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
                ft.Text("예약 목록", size=26, weight=ft.FontWeight.BOLD),
                result_text,
                reservation_column,
            ],
        ),
    )

    refresh_list()

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                header,
                summary_section,
                search_bar,
                reservation_section,
            ],
        ),
    )