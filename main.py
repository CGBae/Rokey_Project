import flet as ft
from pages.login import login_view
from pages.reservation import reservation_view
from pages.admin import admin_view


def main(page: ft.Page):

    page.title = "예약 시스템"
    page.window_width = 1200
    page.window_height = 700

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(
                text="로그인",
                content=login_view(page),
            ),
            ft.Tab(
                text="예약하기",
                content=reservation_view(page),
            ),
            ft.Tab(
                text="관리자",
                content=admin_view(page),
            ),
        ],
        expand=True,
    )

    page.add(tabs)


ft.app(target=main)