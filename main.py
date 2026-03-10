import flet as ft
from pages.login import login_view


def main(page: ft.Page):
    page.add(login_view(page))


ft.run(main)