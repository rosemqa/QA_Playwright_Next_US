from playwright.sync_api import Page, expect
from components.base_component import BaseComponent
from elements.button import Button
from elements.component import Component


class DrawerComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.drawer = Component(page, '[data-testid="next-drawer"] .MuiPaper-root', 'Drawer')
        self.close_button = Button(page, '[data-testid="drawer-close-button"]', 'Close Drawer')

    def close_drawer(self):
        self.close_button.click()

    def check_drawer_is_visible(self):
        self.drawer.check_visible()

    def check_drawer_is_closed(self):
        self.drawer.check_missing()
