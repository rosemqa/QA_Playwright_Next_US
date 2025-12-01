from playwright.sync_api import Page
from components.base_component import BaseComponent
from elements.button import Button
from elements.image import Image


class NavbarComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.logo = Button(page, '[data-testid="header-adaptive-brand"]', 'Logo')
        self.favourites_icon = Button(page, '[data-testid="header-favourites"]', 'Favourites')
        self.active_fav_badge = Image(page, '[data-testid="header-fav-badge-active"]', 'Active fav badge')
        self.inactive_fav_badge = Image(
            page, '[data-testid="header-fav-badge-inactive"]', 'Inactive fav badge')
        self.account = Button(page, '[data-testid="header-adaptive-my-account"]', 'My account')
        self.cart = Button(page, '[data-testid="header-shopping-bag"]', 'Cart')
        self.cart_qty = Button(page, '[data-testid="shopping-bag-link-button"]', 'Cart')
        self.checkout = Button(page, '[data-testid="header-adaptive-checkout"] a', 'Checkout')

    def get_cart_qty(self):
        return self.cart_qty.get_text()

    def check_cart_quantity(self, qty: int | str):
        self.cart_qty.check_have_text(str(qty))

    def check_favorites_badge_is_active(self):
        self.active_fav_badge.check_visible()

    def check_favorites_badge_is_inactive(self):
        self.inactive_fav_badge.check_visible()

    def click_favorites_icon(self):
        self.favourites_icon.click()

    def check_checkout_button_is_enabled(self):
        self.checkout.check_enabled()

    def check_checkout_button_is_disabled(self):
        self.checkout.check_disabled()

