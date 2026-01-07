import re
from playwright.sync_api import Page
from components.base_component import BaseComponent
from data.constants import Placeholders
from data.links import URL
from elements.button import Button
from elements.component import Component
from elements.image import Image
from elements.input import Input
from elements.link import Link


class NavbarComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.logo = Button(page, '[data-testid="header-adaptive-brand"]', 'Logo')
        self.search_input = Input(page, 'input#header-big-screen-search-box', 'Search')
        self.clear_search_input_btn = Button(
            page, '[data-testid="header-search-bar-clear-text-button"]', 'Clear search field')
        self.search_btn = Button(page, '[data-testid="header-search-bar-button"]', 'Search')
        self.recent_searches_modal = Component(
            page, '[data-testid="header-simple-recent-searches"]', 'Recent searches')
        self.clear_recent_searches_btn = Button(
            page, '[data-testid="header-recent-searches-clear-button"]', 'Clear recent searches')
        self.recent_searches_item = Link(
            page, 'a[data-testid*="header-recent-searches-"]', 'Recent searches item')
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

    def enter_search_query(self, search_query: str):
        self.search_input.fill(search_query)

    def click_clear_search_field_btn(self):
        self.clear_search_input_btn.click()

    def click_search_icon(self):
        self.search_btn.click()

    def click_search_field(self):
        self.search_input.click()

    def click_clear_recent_searches_btn(self):
        self.clear_recent_searches_btn.click()

    def click_account_btn(self):
        self.account.click()

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

    def check_placeholder_in_search_input(self):
        placeholder_value = Placeholders.SEARCH_INPUT
        self.search_input.check_has_attribute('placeholder', re.compile(placeholder_value))

    def check_search_input_has_value(self, value: str):
        self.search_input.check_has_value(value=value)

    def check_search_input_is_empty(self):
        self.search_input.check_has_value(value='')

    def check_recent_searches_item_link(self, search_query: str):
        self.recent_searches_item.check_has_attribute(name='href', value=re.compile(f'{URL.SRP}\\?w={search_query}'))

    def check_recent_searches_present(self):
        self.recent_searches_modal.check_visible()

    def check_recent_searches_missing(self):
        self.recent_searches_modal.check_not_visible()
