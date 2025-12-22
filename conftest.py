import time
from datetime import datetime
import allure
import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from pages.cart_page import CartPage
from pages.favorites_page import FavoritesPage
from pages.product_listing_page import ProductListingPage
from pages.product_page import ProductPage


@pytest.fixture(scope='session')
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=True,
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Page:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir='./videos'
    )
    context.tracing.start(snapshots=True, screenshots=True, sources=True)
    page = context.new_page()
    page.set_default_timeout(timeout=10000)
    yield page
    tracing_file = f'./tracing/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip'
    context.tracing.stop(path=tracing_file)
    context.close()

    allure.attach.file(tracing_file, name='trace', extension='zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)


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
