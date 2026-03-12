import flet as ft
from db import get_reservations, approve_reservation


def show_admin(page: ft.Page, show_login, user_id):
    page.clean()
    page.padding = 20
    page.bgcolor = "#f5f6fa"

    reservation_column = ft.Column(spacing=12)
    result_text = ft.Text(value="", size=14, color=ft.Colors.BLUE_600)

    def make_reservation_card(reservation):
        reservation_id = reservation[0]
        login_id = reservation[1]
        name = reservation[2]
        phone = reservation[3]
        date = reservation[4]
        time = reservation[5]
        service = reservation[6]
        approved = reservation[7]

        status_text = "승인" if approved == 1 else "대기"
        status_bg = "#E8F5E9" if approved == 1 else "#FFF3E0"
        status_color = "#2E7D32" if approved == 1 else "#EF6C00"

        def approve_click(e):
            success = approve_reservation(reservation_id, user_id)

            if success:
                result_text.value = f"{reservation_id}번 예약이 승인되었습니다."
                refresh_reservations()
            else:
                result_text.value = "관리자만 승인할 수 있습니다."

            page.update()

        button = ft.ElevatedButton(
            "승인",
            on_click=approve_click,
            disabled=(approved == 1),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

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
                                f"{name} / {service}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Container(
                                padding=ft.Padding(10, 5, 10, 5),
                                border_radius=20,
                                bgcolor=status_bg,
                                content=ft.Text(
                                    status_text,
                                    size=12,
                                    color=status_color,
                                    weight=ft.FontWeight.W_600,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(f"예약번호: {reservation_id}", size=14),
                    ft.Text(f"로그인 계정: {login_id}", size=14),
                    ft.Text(f"연락처: {phone}", size=14),
                    ft.Text(f"예약 일시: {date} {time}", size=14),
                    button,
                ],
            ),
        )

    def refresh_reservations():
        reservation_column.controls.clear()
        rows = get_reservations()

        for r in rows:
            reservation_column.controls.append(make_reservation_card(r))

        page.update()

    def count_waiting():
        rows = get_reservations()
        return len([r for r in rows if r[7] == 0])

    def count_approved():
        rows = get_reservations()
        return len([r for r in rows if r[7] == 1])

    rows = get_reservations()

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
                        ft.Text("전체 예약", size=15, color=ft.Colors.GREY_700),
                        ft.Text(str(len(rows)), size=30, weight=ft.FontWeight.BOLD),
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
                        ft.Text(str(count_waiting()), size=30, weight=ft.FontWeight.BOLD),
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
                        ft.Text("승인 예약", size=15, color=ft.Colors.GREY_700),
                        ft.Text(str(count_approved()), size=30, weight=ft.FontWeight.BOLD),
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
                result_text,
                reservation_column,
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

    refresh_reservations()