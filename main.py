import flet as ft
from pages.login import show_login
from pages.signup import show_signup
from pages.admin_page import show_admin
from pages.user_page import show_user


def main(page: ft.Page):
    page.title = "예약 프로그램"
    page.window_width = 500
    page.window_height = 700
    page.padding = 0
    page.bgcolor = "#f5f6fa"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    def go_login():
        show_login(page, go_signup, go_admin, go_user)

    def go_signup():
        show_signup(page, go_login)

    def go_admin(user_id):
        show_admin(page, go_login, user_id)

    def go_user(user_id):
        show_user(page, go_login, user_id)

    go_login()


ft.app(target=main)