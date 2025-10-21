import allure
import re
from data.constants import PDP


@allure.epic('PDP')
class TestPDP:
    @allure.title('Can select a size; error appears if a size is not selected')
    def test_select_size(self, check, product_page):
        product_page.open()

        # Check if error appears when adding a product to the cart without selecting a size
        product_page.click_add_to_bag()
        with check:
            product_page.check_size_error_text()

        # Check if a size can be selected and the error has disappeared
        with check:
            product_page.select_and_check_random_size()
        with check:
            product_page.check_size_error_is_missing()

    @allure.title('Can select a color')
    def test_select_color(self, product_page):
        product_page.open()

        default_image = product_page.get_product_image_source()
        default_sku = product_page.get_product_sku_text()

        product_page.select_and_check_random_color()

        current_image = product_page.get_product_image_source()
        current_sku = product_page.get_product_sku_text()

        product_page.check_current_url(re.compile(f'/{current_sku}'))
        assert default_sku != current_sku, 'Product SKU is not changed after selecting a different color'
        assert default_image != current_image, 'Product image is not changed after selecting a different color'

    @allure.title('Can open and close the size guide drawer, can switch between inches and centimeters')
    def test_size_guide_drawer(self, product_page):
        not_active_button_color = 'rgb(255, 255, 255)'
        active_button_color = 'rgb(237, 239, 238)'

        product_page.open()

        product_page.click_size_guide()
        product_page.size_guide_drawer.check_drawer_is_visible()

        product_page.size_guide_drawer.check_inches_btn_color(not_active_button_color)
        product_page.size_guide_drawer.check_cm_btn_color(active_button_color)

        product_page.size_guide_drawer.click_inches_btn()

        product_page.size_guide_drawer.check_inches_btn_color(active_button_color)
        product_page.size_guide_drawer.check_cm_btn_color(not_active_button_color)

        product_page.size_guide_drawer.close_drawer()
        product_page.size_guide_drawer.check_drawer_is_closed()

    @allure.title('Can autoscroll to the reviews section when clicking the reviews link')
    def test_autoscroll_to_reviews_section(self, product_page):
        product_page.open()

        product_page.click_reviews_link()
        product_page.check_reviews_section_is_in_viewport()

    @allure.title('Can load more reviews by clicking "View next reviews" button; check number of downloaded reviews')
    def test_load_more_reviews(self, product_page):
        product_page.open()

        product_page.click_reviews_link()
        product_page.check_load_more_reviews()

    @allure.title('Can zoom a product image; can select a thumb in the image carousel')
    def test_zoome_image(self, product_page):
        product_page.open()

        # ZOOM THE IMAGE AND CHECK THE IMMAGE IS ZOOMED
        product_page.zoom_image()
        product_page.check_image_is_zoomed()

        # CLICK A RANDOM THUMB IN THE CAROUSEL AND CHECK THE ZOOMED IMAGE MATCHES THE SELECTED THUMB
        thumb_src = product_page.click_random_thumb()
        product_page.check_zoomed_image_source(thumb_src)

        # CLOSE THE ZOOMED IMAGE
        product_page.close_zoomed_image()
        product_page.check_zoomed_image_is_closed()

    @allure.title('Can scroll up the page to the top by clicking the Back to Top button')
    def test_scroll_to_top(self, product_page):
        product_page.open()

        product_page.press_page_down()
        product_page.check_back_to_top_btn_is_visible()

        product_page.click_back_to_top_btn()

        product_page.check_page_scrolled_to_top()
        product_page.check_back_to_top_btn_is_hidden()

    @allure.title('Can expand/collapse the product description')
    def test_description(self, product_page):
        product_page.open()

        product_page.check_description_collapsed()

        product_page.click_description_header()
        product_page.check_description_expanded()

        product_page.click_description_header()
        product_page.check_description_collapsed()

    @allure.title('Can add a product to cart')
    def test_add_to_cart(self, check, product_page):
        number_of_products_to_add = 1
        product_page.open()

        with check:
            product_page.check_add_to_bag_btn_text('ADD TO BAG')

        product_page.select_and_check_random_size()
        product_page.click_add_to_bag()

        with check:
            product_page.check_add_to_bag_btn_text('ADDED')
        with check:
            product_page.check_add_to_bag_btn_text('ADD TO BAG', timeout=3000)
        with check:
            product_page.navbar.check_cart_quantity(qty=number_of_products_to_add)

    @allure.description('Check that product title and total in mini cart match the title and price on PDP')
    def test_add_to_mini_cart(self, product_page):
        product_page.open()

        product_price = product_page.get_product_price_value()
        product_title = product_page.get_product_title_text()

        product_page.select_and_check_random_size()
        product_page.click_add_to_bag()

        product_page.mini_cart.check_mini_cart_is_visible()
        product_page.mini_cart.check_product_title_text(product_title)
        product_page.mini_cart.check_total_value(product_price)

    @allure.title('Can add/remove a product to/from favorites as unauthorized user')
    def test_add_to_favorites(self, product_page):
        active_btn_src = PDP.ACTIVE_ADD_TO_FAV_BTN_SRC
        inactive_btn_src = PDP.INACTIVE_ADD_TO_FAV_BTN_SRC
        product_page.open()

        product_page.click_add_to_fav_btn()
        product_page.check_sign_in_pop_up_appears()
        product_page.check_fav_btn_image(active_btn_src)
        product_page.navbar.check_favorites_badge_is_active()
        product_page.check_sign_in_pop_up_disappears(timeout=5000)

        product_page.click_add_to_fav_btn()
        product_page.check_fav_btn_image(inactive_btn_src)
        product_page.navbar.check_favorites_badge_is_inactive()
