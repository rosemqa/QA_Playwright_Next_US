from playwright.sync_api import Page, expect

from components.navbar_component import NavbarComponent
from elements.button import Button
from pages.base_page import BasePage


class MainPage(BasePage):
    PAGE_URL = 'https://www.next.us/en'

    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavbarComponent(page)
        self.account_icon = Button(page, 'header-adaptive-my-account-icon-container-link', 'Account icon')

    def click_account_icon(self):
        self.account_icon.click()
