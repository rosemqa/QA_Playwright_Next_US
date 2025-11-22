from playwright.sync_api import Page
from components.drawer_component import DrawerComponent
from elements.button import Button


class SizeGuideComponent(DrawerComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.inches_btn = Button(page, '[data-testid="toggle-option-0"]', 'INCHES')
        self.cm_btn = Button(page, '[data-testid="toggle-option-1"]', 'CM')

    def click_inches_btn(self):
        self.inches_btn.click()
        self.page.wait_for_timeout(500)

    def click_cm_btn(self):
        self.cm_btn.click()
        self.page.wait_for_timeout(500)

    def check_inches_btn_color(self, color_value: str):
        self.inches_btn.check_css_property('background-color', color_value)

    def check_cm_btn_color(self, color_value: str):
        self.cm_btn.check_css_property('background-color', color_value)
