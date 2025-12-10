import random
import re
import time
import allure
from playwright.sync_api import Page
from components.navbar_component import NavbarComponent
from data.links import URL
from elements.button import Button
from elements.checkbox import Checkbox
from elements.component import Component
from elements.dropdown import Dropdown
from elements.dropdown_item import DropdownItem
from elements.link import Link
from elements.slider import Slider
from elements.text import Text
from pages.base_page import BasePage
from tools.logger import get_logger

logger = get_logger("PLP")


@allure.epic('PLP')
class ProductListingPage(BasePage):
    PAGE_URL = URL.PLP

    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavbarComponent(page)

        self.new_in_filter = Checkbox(page, '[data-testid="plp-facet-checkbox-feat-feat:newin"]', 'New In')
        self.clearance_filter = Checkbox(
            page, '[data-testid="plp-facet-checkbox-feat-feat:sale"]', 'Clearance')
        self.more_less_filters = Button(page, 'div[id*="plp-horizontal-filter-"]', 'MORE/LESS filters')
        self.price_filter = Button(page, '[data-testid="plp-filter-chevron-price"]', 'Price filter')
        self.min_price_handle = Slider(page, '[aria-label="Set minimum value"]', 'MIN price')
        self.max_price_handle = Slider(page, '[aria-label="Set maximum value"]', 'MAX price')
        self.price_range = Text(page, '#plp-price-slider span', 'Price range value')
        self.sort_filter = Dropdown(page, '[data-testid="plp-desktop-sort-button"]', 'Sort')
        self.sort_by_price_asc = DropdownItem(page, '[data-value="price"]', 'Price: Low - High')
        self.sort_by_price_desc = DropdownItem(page, '[data-value="pricerev"]', 'Price: High - Low')
        self.alphabetical_sorting = DropdownItem(page, '[data-value="title"]', 'Alphabetical')
        self.most_popular = DropdownItem(page, '[data-value="popular"]', 'Most popular')
        self.size_filter = Dropdown(page, '[data-testid="plp-filter-chevron-size"]', 'Size filter')
        self.size_item = DropdownItem(page, '[data-testid*="plp-facet-checkbox-size-size:"]', 'Size')
        self.size_item_count = Text(
            page, '[data-testid*="plp-facet-count-label-size-size:"]', 'Size item count')
        self.clear_all_sizes = Button(
            page, '[data-testid="plp-filter-clear-all-button-size"]', 'Clear All sizes')
        self.clear_all_filters = Button(
            page, '[data-testid="plp-horizontal-filter-clear-all"]', 'Clear All Filters')
        self.brand_filter = Dropdown(page, '[data-testid="plp-filter-chevron-brand"]', 'Brand filter')
        self.brand_item = DropdownItem(page, '[data-testid*="plp-facet-checkbox-brand-brand:"]', 'Brand')
        self.filters_second_row = Component(
            page, '[data-testid="horizontal-filter-second-row"]', 'Filters second row')

        self.product_card = Component(page, '[data-testid="plp-product-grid-item"]', 'Product card')
        self.product_title = Text(page, '[data-testid="product_summary_title"]', 'Product title')
        self.product_price = Text(page, '[data-testid="product_summary_was_price"]', 'Product price')
        self.sale_price = Text(page, 'a div:nth-child(1) div', 'Product sale price')
        self.any_price = Text(page, '[data-testid$="_price"]', 'Product was/now price')
        self.color_chips = Component(
            page, '[data-testid="product_summary_colourchips"]', 'Product colourchips')
        self.product_color = Link(page, '[data-testid="product_summary_colourchips"] li a', 'Product color')
        self.favorites_btn = Button(
            page, '[data-testid="product-summary-favourites-button"]', 'Add to favorites')
        self.new_in_tag = Text(page, '[data-testid="product_summary_image_media"] p', 'New In')

        self.products_count = Text(page, 'div .esi-count', 'Products count')
        self.back_to_top_btn = Button(page, '[data-testid="plp-back-to-top-btn"]', 'Back to top')

    def click_more_less_filters_btn(self):
        self.more_less_filters.click()

    def check_filters_second_row_appears(self):
        self.filters_second_row.check_visible()

    def check_filters_second_row_not_visible(self):
        self.filters_second_row.check_not_visible()

    def check_more_less_btn_text(self, text: str):
        self.more_less_filters.check_have_text(text)

    def select_new_in_filter(self):
        self.new_in_filter.click()
        time.sleep(1)

    @allure.step('Check that number of product cards with "New In" tag is equal to the number of all cards')
    def check_new_in_cards_count(self):
        all_cards = self.product_card.get_number_of_elements()
        self.new_in_tag.check_number_of_elements(all_cards)

    def select_clearance_filter(self):
        self.clearance_filter.click()

    @allure.step('Check that all product cards have sale prices')
    def check_sale_price_cards_count(self):
        all_cards = self.product_card.get_number_of_elements()
        self.sale_price.check_number_of_elements(all_cards)

    def click_sort_filter(self):
        self.sort_filter.click()

    def sort_by_price(self, sorting_type: str):
        self.click_sort_filter()
        if sorting_type == 'asc':
            self.sort_by_price_asc.click()
        elif sorting_type == 'desc':
            self.sort_by_price_desc.click()
        time.sleep(1)

    def check_sorting_by_price(self, sorting_type: str):
        step = f'Check that products are sorted by {sorting_type} price'

        self.press_page_down()  # scroll page to load more prices
        time.sleep(1)
        with allure.step(step):
            prices = self.any_price.get_locators()
            price_list = [
                int(price.inner_text().split('$')[1].replace(',', ''))
                for price in prices
                if price.is_visible()
                and 'Was' not in price.inner_text()
                and price.inner_text()
            ]
            logger.info(step)
            if sorting_type == 'asc':
                return price_list == sorted(price_list)
            return price_list == sorted(price_list, reverse=True)

    def sort_alphabetically(self):
        self.sort_filter.click()
        self.alphabetical_sorting.click()
        time.sleep(1)

    def check_alphabetical_sorting(self):
        step = 'Check that products are sorted alphabetically'

        with allure.step(step):
            titles = self.product_title.get_locators()
            titles_list = [title.inner_text() for title in titles]
            logger.info(step)
            return titles_list == sorted(titles_list)

    def sort_by_most_popular(self):
        self.click_sort_filter()
        self.most_popular.click()

    def select_random_size(self):
        self.size_filter.click()
        random_item = random.randint(0, 10)
        self.size_item.click(nth=random_item)
        time.sleep(1)
        size_item_count = self.size_item_count.get_text(random_item)
        return size_item_count

    def get_products_count(self) -> str:
        return self.products_count.get_text()

    def check_products_count(self, count: str):
        self.products_count.check_have_text(count)

    def clear_size_filter(self):
        self.clear_all_sizes.click()

    @allure.step('Select a random brand in the brand filter')
    def select_random_brand(self):
        self.more_less_filters.click()
        self.brand_filter.click()
        random_item = random.randint(1, 20)
        self.brand_item.click(nth=random_item)
        selected_brand = self.brand_item.get_text(random_item).split('\n')[0].lower()
        time.sleep(2)
        return selected_brand

    def check_brand_name_in_product_titles(self, brand_name: str):
        step = f'Check that brand_name "{brand_name}" is present in the product titles'

        with allure.step(step):
            titles = self.product_title.get_locators()
            logger.info(step)
            titles_list = [title.inner_text() for title in titles]
            for title in titles_list:
                assert brand_name in title.lower(), f'The selected brand "{brand_name}" not in title "{title}" '

    def click_back_to_top_btn(self):
        self.back_to_top_btn.click()

    def check_back_to_top_btn_is_visible(self):
        self.back_to_top_btn.check_visible()

    def check_back_to_top_btn_is_hidden(self):
        self.back_to_top_btn.check_not_visible()

    def click_price_filter(self):
        self.price_filter.click()

    @allure.step('Set the min price on the price slider')
    def set_min_price(self):
        self.min_price_handle.move_slider(offset_x=random.randint(20, 50))
        time.sleep(1)
        return self.get_min_price_value_in_price_range()

    @allure.step('Set the max price on the price slider')
    def set_max_price(self):
        self.max_price_handle.move_slider(offset_x=random.randint(-50, -20))
        time.sleep(1)
        return self.get_max_price_value_in_price_range()

    def get_min_price_value_in_price_range(self):
        return int(self.price_range.get_text().split()[0].lstrip('$').replace(',', ''))

    def get_max_price_value_in_price_range(self):
        return int(self.price_range.get_text().split()[2].lstrip('$').replace(',', ''))

    def get_price_list(self):
        prices = self.product_price.get_locators()
        price_list = [int(price.inner_text().split()[0].split('$')[1].replace(',', '')) for price in prices]
        return price_list

    def check_min_price(self, min_price):
        step = 'Check that the min price on PLP matches the min price in the price filter'
        price_list = self.get_price_list()
        with allure.step(step):
            logger.info(step)
            assert price_list[0] >= min_price

    def check_max_price(self, max_price):
        step = 'Check that the max price on PLP matches the max price in the price filter'
        price_list = self.get_price_list()
        with allure.step(step):
            logger.info(step)
            assert price_list[0] <= max_price

    def click_clear_all_filters(self):
        self.clear_all_filters.click()

    @allure.step('Add a random product to Favorites')
    def click_add_to_fav_btn(self, nth: int = random.randint(0, 10)):
        self.favorites_btn.click(nth=nth)
        return nth

    def check_add_to_fav_btn_title(self, title_text: str, nth: int = 0):
        self.favorites_btn.check_has_attribute(name='title', value=re.compile(title_text), nth=nth)

    def get_number_of_product_cards(self):
        return self.product_card.get_number_of_elements()

    def check_number_of_product_cards(self, num: int):
        self.product_card.check_number_of_elements(num)

    @allure.step('Hover over a random product color and check that product image has changed')
    def check_hovering_over_product_colors(self):
        # Select a random product colour_chips
        colour_chips = self.color_chips.get_locator(nth=random.randint(0, 5))

        # Get the product image locator of selected colour_chips
        product_card = colour_chips.locator('xpath=ancestor::div[@data-testid="plp-product-grid-item"]')
        product_image = product_card.locator('a[tabindex="0"]>img')

        # Get the product image src in the product card
        initial_image = product_image.get_attribute('src')

        # Get the number of colors in the selected color_chips
        color = colour_chips.locator('li a img')
        number_of_colors = color.count()

        # Hover over a random color except the first one in the selected color_chips
        random_color = color.nth(random.randint(1, number_of_colors - 1))
        random_color.hover()

        # Get the product image src in the product card
        current_image = product_image.get_attribute('src')

        # Check that the product image changed after hovering over a different color
        assert initial_image != current_image, 'Product image did not change when hovering over a different color'
