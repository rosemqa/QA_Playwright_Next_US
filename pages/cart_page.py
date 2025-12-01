import random
from playwright.sync_api import Page
from components.navbar_component import NavbarComponent
from components.recently_viewed_section import RecentlyViewedSection
from data.links import URL
from elements.button import Button
from elements.component import Component
from elements.dropdown import Dropdown
from elements.image import Image
from elements.input import Input
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage


class CartPage(BasePage):
    PAGE_URL = URL.CART_PAGE

    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavbarComponent(page)
        self.recently_viewed_section = RecentlyViewedSection(page)

        self.checkout_btn = Button(page, '.sbm-idCheckoutButton', 'Checkout')
        self.product_image = Image(page, '.sbm-item-detailed-image img', 'Product')
        self.save_for_later_link = Link(page, '.sbm-idSaveForLaterButton', 'Save for later')
        self.remove_item = Link(page, '.sbm-idDeleteButton', 'Remove from cart')
        self.total_price = Text(page, '.sbm-order-total-price', 'Total price')
        self.product_price = Text(page, '#items .sbm-item-price', 'Cart product price')
        self.product_name = Text(page, '.sbm-item-description', 'Cart product name')
        self.size_dropdown = Dropdown(page, '.dk_toggle', 'Size')
        self.qty_input = Input(page, '.qty-count', 'Quantity')
        self.qty_minus = Button(page, '.qty-minus', 'Quantity Minus')
        self.qty_plus = Button(page, '.qty-plus', 'Quantity Plus')
        self.items_count = Text(page, '.shopping-bag-page-title .sbm-item-count', 'Cart items count')
        self.notification = Text(page, '.ShoppingBag .sbm-bag-notification', 'Cart notification')
        self.close_notification = Button(
            page, '.ShoppingBag .CloseNotification', 'Close the cart notification')
        self.items_section = Component(page, '#items', 'Items section')
        self.continue_shopping_btn = Button(page, '.sbm-idContinueShoppingButton', 'Continue shopping')
        self.cart_subtitle = Text(page, '.sb-subtitle', 'Cart subtitle')
        self.view_details_popup = Component(page, '.view-details-popup', 'View details popup')
        self.view_details_product = Link(page, '.view-details-product', 'View details product')
        # SAVED FOR LATER
        self.move_to_bag_link = Link(page, '.sfl-idEditButton', 'Move to bag')
        self.sfl_remove_item = Link(page, '.sfl-item-remove', 'Remove from SFL')
        self.sfl_product_price = Text(page, '.SaveForLater .sbm-item-price', 'SFL product price')
        self.sfl_product_name = Text(page, '.sfl-item-description', 'SFL product name')
        self.sfl_items_count = Text(page, '.sfl-item-count', 'SFL items count')
        self.sfl_notification = Text(page, '.sfl-bag-notification', 'SFL notification')
        self.sfl_close_notification = Button(
            page, '.saved-for-later .CloseNotification', 'Close the SFL notification')
        self.sfl_section = Component(page, '.SaveForLater', 'Saved fo later')

    def get_product_name_text(self):
        return self.product_name.get_text()

    def get_product_price_value(self):
        return int(self.product_price.get_text().lstrip('$').split('.')[0])

    def get_sfl_product_name_text(self):
        return self.sfl_product_name.get_text()

    def get_sfl_product_price_value(self):
        return self.sfl_product_price.get_text()

    def remove_from_cart(self):
        self.remove_item.click()

    def click_save_for_later(self):
        self.save_for_later_link.click()

    def close_cart_notification(self):
        self.close_notification.click()

    def click_move_to_bag(self):
        self.move_to_bag_link.click()

    def close_sfl_notification(self):
        self.sfl_close_notification.click()

    def increase_product_quantity(self):
        random_qty = random.randint(2, 5)
        for i in range(random_qty - 1):
            self.qty_plus.click()
        return random_qty

    def decrease_product_quantity(self, random_qty):
        for i in range(random_qty - 1):
            self.qty_minus.click()

    def click_product_image(self):
        self.product_image.click()

    def click_view_product_details_link(self):
        self.view_details_product.click()

    def check_items_section_is_invisible(self):
        self.items_section.check_not_visible()

    def check_products_count(self, count: str | int):
        if count:
            self.items_count.check_have_text(f'({str(count)})')
        else:
            self.items_count.check_have_text(str(count))

    def check_continue_shopping_btn_is_visible(self):
        self.continue_shopping_btn.check_visible()

    def check_minus_btn_is_enabled(self):
        self.qty_minus.check_enabled()

    def check_minus_btn_is_disabled(self):
        self.qty_minus.check_disabled()

    def check_total_price_value(self, price_value: str | int, qty: int = 1):
        if isinstance(price_value, int):
            self.total_price.check_have_text(f'${str(price_value * qty)}.00')
        else:
            self.total_price.check_have_text(price_value)

    def check_cart_subtitle_text(self, text: str):
        self.cart_subtitle.check_have_text(text)

    def check_sfl_product_name_text(self, product_name: str):
        self.sfl_product_name.check_have_text(product_name)

    def check_cart_product_name_text(self, product_name: str):
        self.product_name.check_have_text(product_name)

    def check_cart_notification_text(self, text: str):
        self.notification.check_visible()
        self.notification.check_have_text(text)

    def check_sfl_count_value(self, count: int):
        self.sfl_items_count.check_have_text(f'({str(count)})')

    def check_cart_notification_is_invisible(self):
        self.notification.check_not_visible()

    def check_sfl_section_is_invisible(self):
        self.sfl_section.check_not_visible()

    def check_sfl_notification_text(self, text: str):
        self.sfl_notification.check_visible()
        self.sfl_notification.check_have_text(text)

    def check_sfl_notification_is_invisible(self):
        self.sfl_notification.check_not_visible()

    def check_view_details_popup_is_open(self):
        self.view_details_popup.check_visible()
