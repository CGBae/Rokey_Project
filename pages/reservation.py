import flet as ft


def reservation_view(page: ft.Page):

    selected_day = None
    selected_time = None

    day_buttons = []
    time_buttons = []

    selected_day_text = ft.Text("선택된 날짜: 없음")
    selected_time_text = ft.Text("선택된 시간: 없음")

    # ---------------- 날짜 선택 ----------------

    def select_day(e):

        nonlocal selected_day

        for btn in day_buttons:
            btn.bgcolor = ft.colors.GREY_200

        e.control.bgcolor = ft.colors.BLUE_200

        selected_day = e.control.data
        selected_day_text.value = f"선택된 날짜: {selected_day}"

        page.update()

    # ---------------- 시간 선택 ----------------

    def select_time(e):

        nonlocal selected_time

        for btn in time_buttons:
            btn.bgcolor = ft.colors.BLUE_100

        e.control.bgcolor = ft.colors.BLUE_400

        selected_time = e.control.data
        selected_time_text.value = f"선택된 시간: {selected_time}:00"

        page.update()

    # ---------------- 달력 ----------------

    days = ["월", "화", "수", "목", "금", "토", "일"]

    day_header = ft.Row(
        [ft.Container(width=40, alignment=ft.alignment.center, content=ft.Text(d)) for d in days],
        spacing=4,
    )

    calendar_rows = []

    day = 1

    for r in range(5):

        row = []

        for c in range(7):

            if day <= 31:

                btn = ft.Container(
                    width=40,
                    height=40,
                    bgcolor=ft.colors.GREY_200,
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text(str(day)),
                    data=day,
                    on_click=select_day,
                )

                day_buttons.append(btn)

                day += 1

            else:

                btn = ft.Container(width=40, height=40)

            row.append(btn)

        calendar_rows.append(ft.Row(row, spacing=4))

    calendar = ft.Column(calendar_rows, spacing=4)

    calendar_box = ft.Container(
        width=360,
        padding=20,
        bgcolor=ft.colors.GREY_100,
        border_radius=10,
        content=ft.Column(
            [
                ft.Text("2026년 3월", size=18),
                day_header,
                calendar,
            ]
        ),
    )

    # ---------------- 시간 ----------------

    times = ["10", "11", "12", "13", "14", "15"]

    time_controls = []

    for t in times:

        btn = ft.Container(
            width=50,
            height=40,
            bgcolor=ft.colors.BLUE_100,
            border_radius=8,
            alignment=ft.alignment.center,
            content=ft.Text(f"{t}:00"),
            data=t,
            on_click=select_time,
        )

        time_buttons.append(btn)
        time_controls.append(btn)

    time_row = ft.Row(time_controls, spacing=6)

    # ---------------- 시술 선택 ----------------

    service_select = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="cut", label="커트"),
                ft.Radio(value="perm", label="펌"),
                ft.Radio(value="color", label="염색"),
                ft.Radio(value="magic", label="매직"),
            ]
        )
    )

    service_box = ft.Container(
        width=380,
        padding=20,
        content=ft.Column(
            [
                ft.Text("시간 선택", size=18),
                time_row,
                selected_day_text,
                selected_time_text,
                ft.Divider(),
                ft.Text("시술 선택", size=18),
                service_select,
                ft.ElevatedButton("예약하기"),
            ]
        ),
    )

    # ---------------- 내 예약 ----------------

    my_reservation = ft.Container(
        width=240,
        padding=20,
        content=ft.Column(
            [
                ft.Text("내 예약", size=18),
                ft.Container(
                    padding=10,
                    bgcolor=ft.colors.GREY_200,
                    border_radius=10,
                    content=ft.Text(
                        "3월 3일\n"
                        "11:00\n"
                        "커트\n"
                        "예약완료"
                    ),
                ),
            ]
        ),
    )

    # ---------------- 전체 레이아웃 ----------------

    return ft.Row(
        [
            calendar_box,
            ft.VerticalDivider(width=1),
            service_box,
            ft.VerticalDivider(width=1),
            my_reservation,
        ],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )