import allure
import random
from playwright.sync_api import Page
from components.mini_cart_component import MiniCartComponent
from components.navbar_component import NavbarComponent
from data.constants import FavPage
from data.links import URL
from elements.component import Component
from elements.dropdown import Dropdown
from elements.dropdown_item import DropdownItem
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage


class FavoritesPage(BasePage):
    PAGE_URL = URL.FAVORITES

    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavbarComponent(page)
        self.mini_cart = MiniCartComponent(page)

        self.product_item = Component(page, '.item-placeholder', 'Product item')
        self.product_name = Text(page, '.item-details .item-description', 'Product name')
        self.remove_item = Link(page, '.remove-item-link', 'Remove item')
        self.add_to_bag = Link(page, '.add-to-bag', 'Add to bag')
        self.moved_to_bag = Text(page, '#moved-to-bag-notification', 'Moved to bag notification')
        self.choose_size = Dropdown(page, '.dk_toggle', 'Choose size')
        self.size_item = DropdownItem(page, '.dk_options li a', 'Size')
        self.no_items = Text(page, '#noItems', 'No items')
        self.items_count = Text(page, '#favouriteItemsCountTarget', 'Items count')

    def get_product_name(self):
        return self.product_name.get_text()

    def click_size_dropdown(self):
        self.choose_size.click()

    def select_random_size(self):
        random_item = random.randint(1, 5)
        self.size_item.click(nth=random_item)
        return self.size_item.get_text(nth=random_item)

    def click_add_to_bag(self):
        self.add_to_bag.click()

    def click_remove_item(self):
        self.remove_item.click()

    def check_moved_to_bag_notification_text(self, text: str):
        self.moved_to_bag.check_visible()
        self.moved_to_bag.check_have_text(text + ' has been moved to your Shopping Bag.')

    @allure.step('Check that moved_to_bag_notification disappears after 8 seconds')
    def check_moved_to_bag_notification_disappears(self):
        self.moved_to_bag.check_not_visible(timeout=8000)
        
    def check_products_count(self, count: int):
        self.items_count.check_have_text(str(count))

    @allure.step('Check the Favorites page is empty')
    def check_favorites_is_empty(self):
        self.product_item.check_not_visible()
        self.no_items.check_visible()
        self.no_items.check_have_text(FavPage.NO_ITEMS)

    def check_size_dropdown_color(self, color_value: str):
        self.choose_size.check_css_property('border-color', color_value)
