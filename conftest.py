import pytest
from playwright.sync_api import sync_playwright, Browser, Page

from pages.main_page import MainPage


@pytest.fixture(scope='session')
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Page:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        no_viewport=True,
        record_video_dir='./videos'
    )
    page = context.new_page()
    page.set_default_timeout(timeout=30000)
    yield page
    context.close()


@pytest.fixture()
def main_page(page):
    return MainPage(page)
