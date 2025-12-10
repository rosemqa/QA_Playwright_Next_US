import time
import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from pages.cart_page import CartPage
from pages.favorites_page import FavoritesPage
from pages.main_page import MainPage
from pages.product_listing_page import ProductListingPage
from pages.product_page import ProductPage


@pytest.fixture(scope='session')
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=True,
            # args=['--start-maximized']
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Page:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        # no_viewport=True,
        # record_video_dir='./videos'
    )
    page = context.new_page()
    page.set_default_timeout(timeout=10000)
    yield page
    context.close()


@pytest.fixture()
def add_to_favorites(page):
    """Add a product to Favourites from PDP"""
    f_page = ProductPage(page)
    f_page.open()
    f_page.click_add_to_fav_btn()
    time.sleep(1)


@pytest.fixture()
def add_to_cart(page):
    """Add a product to cart from PDP"""
    c_page = ProductPage(page)
    c_page.open()
    c_page.select_and_check_random_size()
    c_page.click_add_to_bag()


@pytest.fixture()
def main_page(page):
    return MainPage(page)


@pytest.fixture()
def product_page(page):
    return ProductPage(page)


@pytest.fixture()
def plp(page):
    return ProductListingPage(page)


@pytest.fixture()
def fav_page(page):
    return FavoritesPage(page)


@pytest.fixture()
def cart_page(page):
    return CartPage(page)
