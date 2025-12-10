import random
import allure
import re
from data.links import URL


@allure.epic('PLP')
class TestPLP:
    @allure.title('Can filter by "New In" tag')
    def test_new_in_filter(self, plp):
        plp.open()

        plp.select_new_in_filter()
        # CHECK THAT ALL PRODUCT CARDS HAVE "New In" TAG
        plp.check_new_in_cards_count()

    @allure.title('Can filter by Clearance (sales)')
    def test_clearance_filter(self, plp):
        plp.open()

        plp.select_clearance_filter()
        plp.check_sale_price_cards_count()

    @allure.title('Can show/hide the second row of filters')
    def test_show_filters_second_row(self, plp):
        plp.open()

        plp.check_filters_second_row_not_visible()
        plp.check_more_less_btn_text('MORE')

        plp.click_more_less_filters_btn()
        plp.check_filters_second_row_appears()
        plp.check_more_less_btn_text('LESS')

        plp.click_more_less_filters_btn()
        plp.check_filters_second_row_not_visible()
        plp.check_more_less_btn_text('MORE')

    @allure.title('Can sort by price asc/desc')
    def test_sorting_by_price(self, check, plp):
        plp.open()
        with check:
            plp.sort_by_price(sorting_type='asc')
            assert plp.check_sorting_by_price(sorting_type='asc'), 'Sorting by price asc is incorrect'
        with check:
            plp.sort_by_price(sorting_type='desc')
            assert plp.check_sorting_by_price(sorting_type='desc'), 'Sorting by price desc is incorrect'

    @allure.title('Can sort alphabetically')
    def test_sort_alphabetically(self, plp):
        plp.open()

        plp.sort_alphabetically()
        assert plp.check_alphabetical_sorting(), 'Alphabetical sorting is not correct'

    @allure.title('Can sort by most popular')
    def test_sorting_by_most_popular(self, plp):
        plp.open()

        plp.sort_by_most_popular()
        plp.check_current_url(re.compile(f'{URL.PLP}/f/isort-popular'))

    @allure.title('Can apply and clear the size filter')
    def test_size_filter(self, check, plp):
        plp.open()

        all_products_count = plp.get_products_count()

        with check:
            # APPLY A SIZE FILER AND CHECK THAT ALL PRODUCTS COUNT HAS CHANGED ACCORDINGLY
            filtered_count = plp.select_random_size()
            plp.check_products_count(filtered_count)

        with check:
            # CLEAR THE SIZE FILTER AND CHECK THAT PRODUCTS COUNT HAS RESTORED
            plp.clear_size_filter()
            plp.check_products_count(all_products_count)

    @allure.title('Can filter by brand')
    def test_brand_filter(self, plp):
        plp.open()

        brand_name = plp.select_random_brand()
        plp.check_brand_name_in_product_titles(brand_name=brand_name)

    @allure.title('Can change the price range in thr price filter')
    def test_price_slider(self, check, plp):
        plp.open()

        plp.click_more_less_filters_btn()
        plp.click_price_filter()

        min_price_by_default = plp.get_min_price_value_in_price_range()
        max_price_by_default = plp.get_max_price_value_in_price_range()

        new_min_price = plp.set_min_price()
        new_max_price = plp.set_max_price()
        with check:
            assert new_min_price > min_price_by_default, 'Price range is not changed after moving the min price slider'
        with check:
            assert new_max_price < max_price_by_default, 'Price range is not changed after moving the max price slider'

    @allure.title('Can filter by price range')
    def test_price_filter(self, check, plp):
        plp.open()

        plp.click_more_less_filters_btn()
        plp.click_price_filter()
        min_price = plp.set_min_price()
        max_price = plp.set_max_price()

        plp.sort_by_price('asc')
        with check:
            plp.check_min_price(min_price)

        plp.sort_by_price('desc')
        with check:
            plp.check_max_price(max_price)

    @allure.title('Can clear filters via the "Clear All Filters" button')
    def test_clear_all_filters(self, plp):
        plp.open()

        all_products_count = plp.get_products_count()

        plp.select_new_in_filter()
        plp.select_random_size()

        plp.click_clear_all_filters()
        plp.check_products_count(all_products_count)

    @allure.title('Can scroll up the page to the top by clicking the Back to Top button')
    def test_scroll_to_top(self, plp):
        plp.open()

        plp.press_page_down(n=2)
        plp.check_back_to_top_btn_is_visible()

        plp.click_back_to_top_btn()
        plp.check_page_scrolled_to_top()
        plp.check_back_to_top_btn_is_hidden()

    @allure.title('Can add/remove a product to/from favorites as unauthorized user')
    def test_add_to_favorites(self, plp):
        plp.open()
        # ADD TO FAVORITES
        nth = plp.click_add_to_fav_btn()
        plp.check_add_to_fav_btn_title(title_text='Remove from Favourites:', nth=nth)
        plp.navbar.check_favorites_badge_is_active()
        # REMOVE FROM FAVORITES
        plp.click_add_to_fav_btn()
        plp.check_add_to_fav_btn_title(title_text='Add to Favourites:', nth=nth)
        plp.navbar.check_favorites_badge_is_inactive()

    @allure.title('Check that product cards load when scrolling down the page')
    def test_load_more_products(self, plp):
        default_quantity = 10
        number_of_page_scrolls = random.randint(1, 4)
        plp.open()

        plp.check_number_of_product_cards(default_quantity)
        plp.press_page_down(number_of_page_scrolls)
        plp.check_number_of_product_cards(default_quantity + default_quantity * number_of_page_scrolls)

    @allure.title('Can change a product image when hovering over the different color')
    def test_color(self, plp):
        plp.open()

        plp.check_hovering_over_product_colors()
