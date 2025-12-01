import time
from random import randint
import allure
from playwright.sync_api import Page
from components.mini_cart_component import MiniCartComponent
from components.navbar_component import NavbarComponent
from components.size_guide_component import SizeGuideComponent
from data.constants import PDP
from data.links import URL
from elements.accordeon import Accordion
from elements.button import Button
from elements.component import Component
from elements.dropdown import Dropdown
from elements.image import Image
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage


class ProductPage(BasePage):
    PAGE_URL = URL.PDP

    def __init__(self, page: Page):
        super().__init__(page)
        self.size_guide_drawer = SizeGuideComponent(page)
        self.navbar = NavbarComponent(page)
        self.mini_cart = MiniCartComponent(page)

        self.add_to_bag_btn = Button(page, '[data-testid=item-form-addToBag-button]', 'Add to bag')
        self.favourite_btn = Button(
            page, '[data-testid="item-form-favourite-iconbutton"]', 'Add to favourites')
        self.fav_btn_image = Image(
            page, '[data-testid="item-form-favourite-iconbutton"] img', 'Favorites btn')
        self.product_title = Text(page, '[data-testid="product-title"]', 'Product title')
        self.product_price = Text(page, '[data-testid="product-now-price"]', 'Product price')
        self.size_guide_str = Button(page, '[data-testid="size-guide-link-button"]', 'Size guide')
        self.color_dropdown = Dropdown(page, '[data-testid="colour-select"]', 'Select color')
        self.color_list_item = Dropdown(page, '.MuiList-root li[aria-selected="false"]', 'Color item')
        self.size_dropdown = Dropdown(page, '[data-testid="size-select"]', 'Select size')
        self.size_list_item = Dropdown(page, '.MuiList-root li', 'Size item')
        self.select_size_error = Text(
            page, '[data-testid=item-form-stock-status ] p', 'Select size error')
        self.next_image_btn = Button(page, 'image-action-navigation-right', 'Next image')
        self.prev_image_btn = Button(page, 'image-action-navigation-left', 'Prev image')
        self.reviews_link = Link(page, '[data-testid="item-title-review-stars"]', 'Reviews')
        self.reviews_title = Text(page, '[id="review-card-title"]', 'Reviews title')
        self.product_image = Image(page, '[data-testid="image-gallery-slide-btn"] img', 'Product')
        self.zoom_image_btn = Button(page, '[data-testid="image-gallery-quick-actions"]', 'Zoom image')
        self.zoomed_image = Image(page, '[data-testid="superzoom-image"]', 'Zoomed')
        self.close_zoomed_image_btn = Button(
            page, '[data-testid="image-carousel-quick-actions-close-superzoom"]', 'Close a zoomed image')
        self.thumb = Image(
            page, '[data-testid="superzoom-modal"] [data-testid*="pdp-thumb-"] img', 'Thumb')
        self.view_next_reviews = Button(page, '[data-testid="reviews-load-more"]', 'View next reviews')
        self.review_item = Component(
            page, '[data-testid="reviews-container"] .MuiGrid-container', 'Review')
        self.product_sku = Text(page, '[data-testid="product-code"]', 'Product SKU')
        self.back_to_top_btn = Button(page, '[data-testid="back-to-top"]', 'Back to top')
        self.description_header = Accordion(
            page, '#panel-header', 'Description header')
        self.expanded_description = Accordion(
            page, '[data-testid="item-description-tone-of-voice"]', 'Description content')
        self.sign_in_pop_up = Component(page, '#next-popover-dialog', 'Sign-in pop-up')

    def get_product_title_text(self):
        return self.product_title.get_text()

    def get_product_price_value(self):
        return int(self.product_price.get_text().lstrip('$'))

    def get_product_sku_text(self):
        return self.product_sku.get_text().replace('-', '').lower()

    def get_product_image_source(self):
        return self.product_image.get_image_source()

    @allure.step('Select a random size and check it was selected')
    def select_and_check_random_size(self):
        self.size_dropdown.click()
        random_item = randint(1, 5)
        size_list_item_text = self.size_list_item.get_text(nth=random_item)
        self.size_list_item.click(nth=random_item)
        self.size_dropdown.check_have_text(size_list_item_text)
        return self.size_dropdown.get_text()

    @allure.step('Select a random color and check it was selected')
    def select_and_check_random_color(self):
        self.color_dropdown.click()
        random_item = randint(0, 5)
        color_list_item_text = self.color_list_item.get_text(nth=random_item)
        self.color_list_item.click(nth=random_item)
        self.color_dropdown.check_have_text(color_list_item_text)

    def click_add_to_bag(self):
        self.add_to_bag_btn.click()

    def zoom_image(self):
        self.zoom_image_btn.click()

    def check_image_is_zoomed(self):
        self.zoomed_image.check_visible()

    def close_zoomed_image(self):
        self.close_zoomed_image_btn.click()

    def check_zoomed_image_is_closed(self):
        self.zoomed_image.check_missing()

    def click_random_thumb(self):
        random_thumb = randint(1, 5)
        self.thumb.click(random_thumb)
        return self.thumb.get_image_source(random_thumb)

    def check_zoomed_image_source(self, source):
        self.zoomed_image.check_image_source(source)

    def click_reviews_link(self):
        self.reviews_link.click()

    def check_reviews_section_is_in_viewport(self):
        self.reviews_title.check_in_viewport()

    def check_load_more_reviews(self):
        default_reviews_number = 5
        reviews_number_per_download = 5
        clicks_number = randint(1, 5)
        for i in range(clicks_number):
            self.view_next_reviews.click()
        expected_reviews_number = clicks_number * reviews_number_per_download + default_reviews_number
        self.review_item.check_number_of_elements(number=expected_reviews_number)

    def click_size_guide(self):
        self.size_guide_str.click()

    def check_size_error_text(self):
        self.select_size_error.check_visible()
        self.select_size_error.check_have_text(PDP.SELECT_SIZE_ERROR)

    def check_size_error_is_missing(self):
        self.select_size_error.check_missing()

    def click_back_to_top_btn(self):
        self.back_to_top_btn.click()

    def check_back_to_top_btn_is_visible(self):
        self.back_to_top_btn.check_visible()

    def check_back_to_top_btn_is_hidden(self):
        self.back_to_top_btn.check_not_visible()

    def click_description_header(self):
        self.description_header.click()

    def check_description_expanded(self):
        self.expanded_description.check_visible()

    def check_description_collapsed(self):
        self.expanded_description.check_not_visible()

    def check_add_to_bag_btn_text(self, text, timeout: float = None):
        self.add_to_bag_btn.check_have_text(text, timeout=timeout)

    def check_sign_in_pop_up_appears(self):
        self.sign_in_pop_up.check_visible()

    def check_sign_in_pop_up_disappears(self, timeout):
        with allure.step(f'Check that sign_in_pop disappears after {timeout/1000} seconds'):
            self.sign_in_pop_up.check_not_visible(timeout=timeout)

    def click_add_to_fav_btn(self):
        self.favourite_btn.click()

    def check_fav_btn_image(self, src: str):
        time.sleep(1)
        self.fav_btn_image.check_image_source(src)
