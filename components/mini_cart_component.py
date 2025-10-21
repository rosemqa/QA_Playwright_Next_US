from playwright.sync_api import Page
from components.base_component import BaseComponent
from elements.button import Button
from elements.component import Component
from elements.text import Text


class MiniCartComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.mini_cart = Component(page, '[data-testid="header-mini-shopping-bag"]', 'Mini cart')
        self.product_title = Text(
            page, '[data-testid="header-mini-shopping-bag-item-description"]', 'Product title')
        self.view_bag_btn = Button(page, '[data-ga-v3="View Bag"]', 'View Bag')
        self.checkout_btn = Button(page, '[data-testid="minibag-adaptive-checkout"]', 'Checkout')
        self.total = Text(page, 'span [data-testid="header-mini-shopping-bag-total"]', 'Total')

    def check_product_title_text(self, text: str):
        self.product_title.check_have_text(text, 0)

    def check_total_value(self, value: int):
        self.total.check_have_text(f'${value}.00')

    def check_mini_cart_is_visible(self):
        self.mini_cart.check_visible()
