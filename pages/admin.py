import flet as ft
import calendar


def admin_view(page: ft.Page):

    year = 2026
    month = 3
    week_index = 0

    days = ["월","화","수","목","금","토","일"]
    times = ["10:00","11:00","12:00","13:00","14:00","15:00"]

    schedule_column = ft.Column()
    waiting_column = ft.Column(scroll="auto")

    grid = {}

    # ---------------- 주 계산 ----------------

    def get_weeks():

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(year,month)

        return weeks

    # ---------------- 헤더 업데이트 ----------------

    week_text = ft.Text()

    date_header = ft.Row()

    def update_header():

        weeks = get_weeks()

        if week_index >= len(weeks):
            return

        week = weeks[week_index]

        week_names = ["첫째주","둘째주","셋째주","넷째주","다섯째주"]

        week_text.value = f"{month}월 {week_names[week_index]}"

        date_header.controls.clear()

        date_header.controls.append(ft.Container(width=60))

        for d in week:

            if d == 0:
                txt = ""
            else:
                txt = f"{month}/{d}"

            date_header.controls.append(
                ft.Container(
                    width=80,
                    alignment=ft.alignment.center,
                    content=ft.Text(txt)
                )
            )

        page.update()

    # ---------------- 주 이동 ----------------

    def prev_week(e):

        nonlocal week_index

        if week_index > 0:
            week_index -= 1

        update_header()

    def next_week(e):

        nonlocal week_index

        weeks = get_weeks()

        if week_index < len(weeks)-1:
            week_index += 1

        update_header()

    week_header = ft.Row(
        [
            ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=prev_week),

            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=week_text
            ),

            ft.IconButton(icon=ft.icons.ARROW_FORWARD,on_click=next_week)
        ]
    )

    schedule_column.controls.append(week_header)
    schedule_column.controls.append(date_header)

    # ---------------- 시간표 ----------------

    for t in times:

        row_controls = [
            ft.Container(
                content=ft.Text(t),
                width=60,
                alignment=ft.alignment.center
            )
        ]

        for d in days:

            box = ft.Container(
                width=80,
                height=60,
                bgcolor="blue100",
                border_radius=6,
                alignment=ft.alignment.center
            )

            grid[(d,t)] = box

            row_controls.append(box)

        schedule_column.controls.append(ft.Row(row_controls))

    # ---------------- 예약 승인 ----------------

    def approve(e):

        day,time,service,container = e.control.data

        box = grid[(day,time)]

        box.bgcolor = "green300"
        box.content = ft.Text(service)

        waiting_column.controls.remove(container)

        page.update()

    # ---------------- 예약 취소 ----------------

    def cancel(e):

        container = e.control.data

        waiting_column.controls.remove(container)

        page.update()

    # ---------------- 예약 대기 ----------------

    reservations = [
        ("월","10:00","커트"),
        ("화","11:00","펌"),
        ("수","12:00","염색"),
        ("목","13:00","매직"),
    ]

    for r in reservations:

        day,time,service = r

        card = ft.Container()

        approve_btn = ft.ElevatedButton("승인")
        cancel_btn = ft.OutlinedButton("취소")

        approve_btn.data = (day,time,service,card)
        cancel_btn.data = card

        approve_btn.on_click = approve
        cancel_btn.on_click = cancel

        card.content = ft.Column(
            [
                ft.Text(f"{day} {time} {service}"),
                ft.Row([approve_btn,cancel_btn])
            ]
        )

        card.padding = 10
        card.bgcolor = "red300"
        card.border_radius = 10

        waiting_column.controls.append(card)

    # ---------------- 초기 헤더 ----------------

    update_header()

    # ---------------- 레이아웃 ----------------

    layout = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("시간표",size=22),
                    schedule_column
                ],
                expand=True
            ),

            ft.VerticalDivider(),

            ft.Column(
                [
                    ft.Text("예약 대기",size=22),
                    waiting_column
                ],
                width=260
            )
        ],
        expand=True
    )

    return ft.Container(
        padding=30,
        expand=True,
        content=layout
    )