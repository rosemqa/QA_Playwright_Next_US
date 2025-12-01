import allure
import re
import time
from data.constants import Bag
from data.links import URL


@allure.epic('Cart page')
class TestCartPage:
    @allure.title('Can remove a product from the cart')
    def test_remove_product(self, check, add_to_cart, cart_page):
        cart_page.open()
        with check:
            cart_page.navbar.check_checkout_button_is_enabled()
        with check:
            cart_page.check_products_count(1)

        cart_page.remove_from_cart()
        with check:
            cart_page.check_items_section_is_invisible()
        with check:
            cart_page.check_products_count('')
        with check:
            cart_page.check_continue_shopping_btn_is_visible()
        with check:
            cart_page.navbar.check_checkout_button_is_disabled()
        with check:
            cart_page.navbar.check_cart_quantity(0)
        with check:
            cart_page.check_cart_subtitle_text(Bag.EMPTY_BAG)
        with check:
            cart_page.check_total_price_value(0)

    @allure.title('Can move a product to the Saved for Later section')
    def test_save_for_later(self, check, add_to_cart, cart_page):
        cart_page.open()
        product_name = cart_page.get_product_name_text()

        cart_page.click_save_for_later()
        with check:
            cart_page.check_items_section_is_invisible()
        with check:
            cart_page.check_sfl_product_name_text(product_name=product_name)
        with check:
            cart_page.check_cart_notification_text(text=Bag.MOVED_TO_SFL(product_name))
        with check:
            cart_page.check_sfl_count_value(1)
        with check:
            cart_page.navbar.check_checkout_button_is_disabled()
        # CART NOTIFICATION CAN BE CLOSED
        cart_page.close_cart_notification()
        with check:
            cart_page.check_cart_notification_is_invisible()

    @allure.title('Can move a product from SFL to the Bag')
    def test_move_to_bag(self, check, add_to_cart, cart_page):
        cart_page.open()
        cart_page.click_save_for_later()
        sfl_product_name = cart_page.get_sfl_product_name_text()
        sfl_product_price = cart_page.get_sfl_product_price_value()
        cart_page.check_items_section_is_invisible()

        cart_page.click_move_to_bag()
        with check:
            cart_page.check_sfl_section_is_invisible()
        with check:
            cart_page.check_cart_product_name_text(product_name=sfl_product_name)
        with check:
            cart_page.check_sfl_count_value(0)
        with check:
            cart_page.check_sfl_notification_text(Bag.MOVED_TO_BAG)
        with check:
            cart_page.navbar.check_checkout_button_is_enabled()
        with check:
            cart_page.check_total_price_value(price_value=sfl_product_price)
        # SFL NOTIFICATION CAN BE CLOSED
        cart_page.close_sfl_notification()
        with check:
            cart_page.check_sfl_notification_is_invisible()

    @allure.title('Can change the product quantity by clicking "+" and "-" buttons')
    def test_change_product_quantity(self, check, add_to_cart, cart_page):
        cart_page.open()
        product_price = cart_page.get_product_price_value()

        qty = cart_page.increase_product_quantity()
        with check:
            cart_page.check_products_count(count=qty)
        with check:
            cart_page.check_total_price_value(price_value=product_price, qty=qty)
        with check:
            cart_page.navbar.check_cart_quantity(qty=qty)
        with check:
            cart_page.check_minus_btn_is_enabled()

        cart_page.decrease_product_quantity(random_qty=qty)

        cart_page.check_products_count(count=1)
        cart_page.check_total_price_value(price_value=product_price)
        cart_page.navbar.check_cart_quantity(qty=1)
        cart_page.check_minus_btn_is_disabled()

    @allure.title('Check that the view_product_details link leads to relevant PDP')
    def test_view_product_details(self, add_to_cart, cart_page):
        cart_page.open()
        time.sleep(10)

        cart_page.click_product_image()
        cart_page.check_view_details_popup_is_open()

        cart_page.click_view_product_details_link()
        cart_page.check_current_url(re.compile(URL.PDP))

    @allure.title('Check the recently viewed section contains the relevant product and can be cleared')
    def test_recently_viewed_section(self, add_to_cart, cart_page):
        cart_page.open()
        product_price = cart_page.get_product_price_value()

        cart_page.recently_viewed_section.check_product_price(product_price)

        cart_page.recently_viewed_section.click_clear_all_btn()
        cart_page.recently_viewed_section.check_section_is_empty()
