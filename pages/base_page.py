import time

from typing import Literal, Pattern

import allure
from tools.logger import get_logger
from playwright.sync_api import Page, TimeoutError, expect

logger = get_logger('BASE_PAGE')


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # def open(self, url: str):
    #     step = f'Go to url "{url}"'
    #
    #     with allure.step(step):
    #         logger.info(step)
    #         self.page.goto(self.PAGE_URL)

    def open(self):
        step = f'Go to url "{self.PAGE_URL}"'

        with allure.step(step):
            logger.info(step)
            self.page.goto(self.PAGE_URL, wait_until="domcontentloaded")
            self.accept_cookies()
            self.close_country_selector()

    def check_current_url(self, expected_url: Pattern[str]):
        step = f'Check that current url matches pattern "{expected_url.pattern}"'
        with allure.step(step):
            logger.info(step)
            expect(self.page).to_have_url(expected_url)

    # noinspection PyTypeChecker
    def is_element_present(self, locator: str, timeout=10, state='attached') -> bool:
        try:
            self.page.locator(locator).wait_for(timeout=timeout * 1000, state=state)
        except TimeoutError:
            return False
        return True

    @allure.step('Accept cookies')
    def accept_cookies(self):
        if self.is_element_present(locator='#onetrust-accept-btn-handler'):
            self.page.locator('#onetrust-accept-btn-handler').click()

    @allure.step('Close country selector')
    def close_country_selector(self):
        if self.is_element_present(locator='[data-testid="country-selector-close-button"]'):
            self.page.get_by_test_id('country-selector-close-button').click()

    def press_page_down(self, n: int = 1):
        step = f'Press the Page Down key {n} times'

        with allure.step(step):
            logger.info(step)
            self.page.focus("body")
            for _ in range(n):
                self.page.keyboard.press('PageDown')
                time.sleep(2)

    def check_page_scrolled_to_top(self):
        step = 'Check that page is scrolled to the top'

        with allure.step(step):
            logger.info(step)
            scroll_position = self.page.evaluate("window.scrollY")
            assert scroll_position == 0, 'The page is not scrolled to the top'

    def drag_and_drop_by_offset(self, selector, offset_x=0, offset_y=0):
        step = f'Drag and drop an element by offset'

        with allure.step(step):
            element = self.page.query_selector(selector)
            box = element.bounding_box()
            start_x = box['x'] + box['width'] / 2
            start_y = box['y'] + box['height'] / 2
            logger.info(step)
            self.page.mouse.move(start_x, start_y)
            self.page.mouse.down()
            self.page.mouse.move(start_x + offset_x, start_y + offset_y, steps=10)
            self.page.mouse.up()
