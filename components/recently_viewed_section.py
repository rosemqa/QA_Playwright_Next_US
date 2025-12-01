from playwright.sync_api import Page
from components.base_component import BaseComponent
from data.constants import RecentlyViewed
from elements.button import Button
from elements.component import Component
from elements.text import Text


class RecentlyViewedSection(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.clear_all_btn = Button(page, 'button.clear', 'Clear All')
        self.recently_viewed_product = Component(page, '#rvList li', 'Recently viewed product')
        self.empty_section_text = Text(page, '.cleared', 'Empty recently_viewed')

    def click_clear_all_btn(self):
        self.clear_all_btn.click()

    def check_product_price(self, price_value: int):
        self.recently_viewed_product.check_visible()
        self.recently_viewed_product.check_have_text(f'${str(price_value)}')

    def check_section_is_empty(self):
        self.recently_viewed_product.check_not_visible()
        self.empty_section_text.check_have_text(RecentlyViewed.empty_section)
