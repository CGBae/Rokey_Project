import calendar
from datetime import date, datetime

import flet as ft
from db import get_reservations, approve_reservation


def show_admin(page: ft.Page, show_login, user_id):
    page.clean()
    page.padding = 20
    page.bgcolor = "#f5f6fa"
    page.scroll = ft.ScrollMode.AUTO

    current_month = date.today().replace(day=1)
    selected_date = date.today()

    result_text = ft.Text(value="", size=14, color=ft.Colors.BLUE_600)

    calendar_grid = ft.GridView(
        runs_count=7,
        max_extent=150,
        child_aspect_ratio=0.95,
        spacing=10,
        run_spacing=10,
        expand=True,
    )

    reservation_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)

    month_title = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    selected_date_text = ft.Text("", size=16, color=ft.Colors.GREY_700)

    total_count = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)
    waiting_count = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)
    approved_count = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)

    weekday_row = ft.Row(
        spacing=10,
        controls=[
            ft.Container(
                expand=1,
                alignment=ft.Alignment.CENTER,
                padding=10,
                content=ft.Text(day, weight=ft.FontWeight.BOLD),
            )
            for day in ["월", "화", "수", "목", "금", "토", "일"]
        ],
    )

    def parse_reservation_date(value):
        return datetime.strptime(value, "%Y-%m-%d").date()

    def get_all_rows():
        return get_reservations()

    def get_rows_for_month(year, month):
        rows = get_all_rows()
        filtered = []
        for r in rows:
            try:
                d = parse_reservation_date(r[4])
                if d.year == year and d.month == month:
                    filtered.append(r)
            except Exception:
                continue
        return filtered

    def get_rows_for_selected_date():
        rows = get_all_rows()
        filtered = []
        for r in rows:
            try:
                d = parse_reservation_date(r[4])
                if d == selected_date:
                    filtered.append(r)
            except Exception:
                continue
        return filtered

    def status_badge(approved):
        status_text = "승인" if approved == 1 else "대기"
        status_bg = "#E8F5E9" if approved == 1 else "#FFF3E0"
        status_color = "#2E7D32" if approved == 1 else "#EF6C00"

        return ft.Container(
            padding=ft.Padding(10, 5, 10, 5),
            border_radius=20,
            bgcolor=status_bg,
            content=ft.Text(
                status_text,
                size=12,
                color=status_color,
                weight=ft.FontWeight.W_600,
            ),
        )

    def make_reservation_card(reservation):
        reservation_id = reservation[0]
        login_id = reservation[1]
        name = reservation[2]
        phone = reservation[3]
        reserve_date = reservation[4]
        reserve_time = reservation[5]
        service = reservation[6]
        approved = reservation[7]

        def approve_click(e):
            success = approve_reservation(reservation_id, user_id)
            if success:
                result_text.value = f"{reservation_id}번 예약이 승인되었습니다."
            else:
                result_text.value = "관리자만 승인할 수 있습니다."
            refresh_all()

        return ft.Container(
            padding=18,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, "#E5E7EB"),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"{name} / {service}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            status_badge(approved),
                        ],
                    ),
                    ft.Text(f"예약번호: {reservation_id}", size=13),
                    ft.Text(f"로그인 계정: {login_id}", size=13),
                    ft.Text(f"연락처: {phone}", size=13),
                    ft.Text(f"예약 일시: {reserve_date} {reserve_time}", size=13),
                    ft.ElevatedButton(
                        "승인",
                        on_click=approve_click,
                        disabled=(approved == 1),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ],
            ),
        )

    def refresh_summary():
        rows = get_all_rows()
        total_count.value = str(len(rows))
        waiting_count.value = str(len([r for r in rows if r[7] == 0]))
        approved_count.value = str(len([r for r in rows if r[7] == 1]))

    def refresh_selected_day_list():
        reservation_column.controls.clear()
        rows = get_rows_for_selected_date()

        selected_date_text.value = f"선택한 날짜: {selected_date.strftime('%Y-%m-%d')}"

        if not rows:
            reservation_column.controls.append(
                ft.Container(
                    padding=20,
                    border_radius=16,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, "#E5E7EB"),
                    content=ft.Text("선택한 날짜의 예약이 없습니다.", size=15),
                )
            )
        else:
            rows.sort(key=lambda x: x[5])
            for r in rows:
                reservation_column.controls.append(make_reservation_card(r))

    def build_day_cell(cell_date, month_rows, is_current_month):
        rows_for_day = []
        waiting = 0
        approved = 0

        for r in month_rows:
            try:
                d = parse_reservation_date(r[4])
                if d == cell_date:
                    rows_for_day.append(r)
                    if r[7] == 1:
                        approved += 1
                    else:
                        waiting += 1
            except Exception:
                continue

        is_selected = cell_date == selected_date
        is_today = cell_date == date.today()
        has_reservation = len(rows_for_day) > 0

        if not is_current_month:
            bg = "#F1F3F5"
            border_color = "#E5E7EB"
            border_width = 1
            day_color = ft.Colors.GREY_500
        else:
            bg = ft.Colors.WHITE
            border_color = "#E5E7EB"
            border_width = 1
            day_color = ft.Colors.BLACK

            if has_reservation:
                border_color = "#111111"
                border_width = 2

            if is_today:
                bg = "#F8FBFF"
                day_color = "#1565C0"

            if is_selected:
                bg = "#EAF2FF"
                border_color = "#111111"
                border_width = 1
                day_color = "#1E5EFF"

        preview_controls = []
        sorted_rows = sorted(rows_for_day, key=lambda x: x[5])

        for r in sorted_rows[:3]:
            status_bg = "#E8F5E9" if r[7] == 1 else "#FFF3E0"
            status_color = "#2E7D32" if r[7] == 1 else "#EF6C00"

            preview_controls.append(
                ft.Container(
                    padding=ft.Padding(6, 3, 6, 3),
                    border_radius=8,
                    bgcolor=status_bg,
                    content=ft.Text(
                        f"{r[5]} {r[2]}",
                        size=10,
                        color=status_color,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                )
            )

        if len(sorted_rows) > 3:
            more_count = len(sorted_rows) - 3
            preview_controls.append(
                ft.Text(
                    f"+{more_count} more",
                    size=10,
                    color=ft.Colors.GREY_700,
                    weight=ft.FontWeight.BOLD,
                )
            )

        if not rows_for_day:
            preview_controls.append(
                ft.Text("예약 없음", size=10, color=ft.Colors.GREY_500)
            )

        count_row = ft.Row(
            spacing=6,
            controls=[
                ft.Container(
                    padding=ft.Padding(6, 2, 6, 2),
                    border_radius=10,
                    bgcolor="#FFF3E0",
                    content=ft.Text(
                        f"대기 {waiting}",
                        size=9,
                        color="#EF6C00",
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(6, 2, 6, 2),
                    border_radius=10,
                    bgcolor="#E8F5E9",
                    content=ft.Text(
                        f"승인 {approved}",
                        size=9,
                        color="#2E7D32",
                    ),
                ),
            ],
        )

        def select_day(e):
            nonlocal selected_date
            selected_date = cell_date
            refresh_all()

        return ft.Container(
            on_click=select_day,
            ink=True,
            padding=10,
            border_radius=14,
            bgcolor=bg,
            border=ft.border.all(border_width, border_color),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                str(cell_date.day),
                                size=17,
                                weight=ft.FontWeight.BOLD,
                                color=day_color,
                            ),
                            ft.Text(
                                f"{len(rows_for_day)}건",
                                size=10,
                                color=ft.Colors.GREY_700,
                            ),
                        ],
                    ),
                    count_row,
                    ft.Column(
                        spacing=4,
                        controls=preview_controls,
                    ),
                ],
            ),
        )

    def refresh_calendar():
        calendar_grid.controls.clear()

        year = current_month.year
        month = current_month.month
        month_title.value = f"{year}년 {month}월"

        month_rows = get_rows_for_month(year, month)
        month_matrix = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)

        for week in month_matrix:
            for d in week:
                calendar_grid.controls.append(
                    build_day_cell(d, month_rows, d.month == month)
                )

    def refresh_all():
        refresh_summary()
        refresh_calendar()
        refresh_selected_day_list()
        page.update()

    def go_prev_month(e):
        nonlocal current_month
        if current_month.month == 1:
            current_month = current_month.replace(year=current_month.year - 1, month=12)
        else:
            current_month = current_month.replace(month=current_month.month - 1)
        refresh_all()

    def go_next_month(e):
        nonlocal current_month
        if current_month.month == 12:
            current_month = current_month.replace(year=current_month.year + 1, month=1)
        else:
            current_month = current_month.replace(month=current_month.month + 1)
        refresh_all()

    def go_today(e):
        nonlocal current_month, selected_date
        selected_date = date.today()
        current_month = selected_date.replace(day=1)
        refresh_all()

    def on_picker_change(e):
        nonlocal current_month, selected_date
        if month_picker.value:
            selected_date = month_picker.value
            current_month = month_picker.value.replace(day=1)
            refresh_all()

    month_picker = ft.DatePicker(
        help_text="날짜 선택",
        confirm_text="확인",
        cancel_text="취소",
        on_change=on_picker_change,
    )

    def open_month_picker(e):
        page.show_dialog(month_picker)

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
                width=170,
                padding=20,
                border_radius=18,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, "#E5E7EB"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("전체 예약", size=15, color=ft.Colors.GREY_700),
                        total_count,
                    ],
                ),
            ),
            ft.Container(
                width=170,
                padding=20,
                border_radius=18,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, "#E5E7EB"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("대기 예약", size=15, color=ft.Colors.GREY_700),
                        waiting_count,
                    ],
                ),
            ),
            ft.Container(
                width=170,
                padding=20,
                border_radius=18,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, "#E5E7EB"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("승인 예약", size=15, color=ft.Colors.GREY_700),
                        approved_count,
                    ],
                ),
            ),
        ],
    )

    month_toolbar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=8,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        tooltip="이전 달",
                        on_click=go_prev_month,
                    ),
                    month_title,
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_RIGHT,
                        tooltip="다음 달",
                        on_click=go_next_month,
                    ),
                ],
            ),
            ft.Row(
                spacing=8,
                controls=[
                    ft.OutlinedButton(
                        "오늘로 이동",
                        on_click=go_today,
                    ),
                    ft.ElevatedButton(
                        "날짜 선택",
                        on_click=open_month_picker,
                    ),
                ],
            ),
        ],
    )

    calendar_card = ft.Container(
        expand=7,
        padding=20,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, "#E5E7EB"),
        content=ft.Column(
            expand=True,
            spacing=16,
            controls=[
                ft.Text("월간 예약 달력", size=24, weight=ft.FontWeight.BOLD),
                month_toolbar,
                weekday_row,
                ft.Container(
                    expand=True,
                    content=calendar_grid,
                ),
            ],
        ),
    )

    detail_card = ft.Container(
        expand=4,
        padding=20,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, "#E5E7EB"),
        content=ft.Column(
            expand=True,
            spacing=16,
            controls=[
                ft.Text("예약 상세", size=24, weight=ft.FontWeight.BOLD),
                selected_date_text,
                result_text,
                ft.Container(
                    expand=True,
                    content=reservation_column,
                ),
            ],
        ),
    )

    main_content = ft.Row(
        expand=True,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            calendar_card,
            detail_card,
        ],
    )

    page.add(
        ft.Column(
            expand=True,
            spacing=20,
            controls=[
                header,
                summary_row,
                main_content,
            ],
        )
    )

    refresh_all()