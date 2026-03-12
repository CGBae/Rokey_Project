import flet as ft


def show_admin(page: ft.Page, show_login, user_id):
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