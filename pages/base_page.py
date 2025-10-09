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
            self.page.goto(self.PAGE_URL)
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
        self.page.locator('#onetrust-accept-btn-handler').click()

    @allure.step('Close country selector')
    def close_country_selector(self):
        if self.is_element_present(locator='[data-testid="country-selector-close-button"]', timeout=2):
            self.page.get_by_test_id('country-selector-close-button').click()
