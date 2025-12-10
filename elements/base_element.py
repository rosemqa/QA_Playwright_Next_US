import allure
from typing import Pattern
from playwright.sync_api import Page, expect, Locator
from tools.logger import get_logger

logger = get_logger('BASE_ELEMENT')


class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.locator = locator
        self.name = name

    @property
    def type_of(self) -> str:
        return 'base_element'

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Get locator "{locator}" at index "{nth}"'

        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator).nth(nth)

    def get_nested_locator(self, nested_selector: str, loc_nth: int = 0, nest_nth: int = 0, **kwargs):
        nested_locator = self.get_locator(loc_nth, **kwargs).locator(nested_selector).nth(nest_nth)
        return nested_locator

    def get_locators(self, **kwargs):
        locator = self.locator.format(**kwargs)
        step = f'Get a list of "{locator}" locators'

        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator).all()

    def click(self, nth: int = 0, **kwargs):
        step = f'Click {self.type_of} "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.click()

    def check_visible(self, nth: int = 0, **kwargs):
        step = f'Check that {self.type_of} "{self.name}" is visible'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_visible()

    def check_not_visible(self, timeout: float = None, nth: int = 0, **kwargs):
        step = f'Check that {self.type_of} "{self.name}" is not visible'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).not_to_be_visible(timeout=timeout)

    def check_missing(self, nth: int = 0, **kwargs):
        step = f'Check that {self.type_of} "{self.name}" is missing'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).not_to_be_attached()

    def get_text(self, nth: int = 0, **kwargs):
        step = f'Get text of the "{self.name}" {self.type_of}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(f'{step}: {locator.inner_text()}')
            return locator.inner_text()

    def check_have_text(self, text: str, timeout: float = None, nth: int = 0, **kwargs):
        step = f'Check that {self.type_of} "{self.name}" has text "{text}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_text(text, timeout=timeout, use_inner_text=True)

    def get_number_of_elements(self):
        step = f'Get number of "{self.name}" {self.type_of}s'

        with allure.step(step):
            locator = self.page.locator(self.locator)
            logger.info(step)
            return locator.count()

    def check_number_of_elements(self, number: int):
        step = f'Check that number of "{self.name}" {self.type_of}s is {number}'

        with allure.step(step):
            locator = self.page.locator(self.locator)
            logger.info(step)
            expect(locator).to_have_count(number)

    def hover_over(self, nth: int = 0, **kwargs):
        step = f'Hover over "{self.name}" {self.type_of}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.hover()

    def check_css_property(self, property_name: str, property_value: str, nth: int = 0, **kwargs):
        step = f'Check css property "{property_name}" of the "{self.name}" {self.type_of} has value {property_value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            current_property_value = locator.evaluate(
                f"element => getComputedStyle(element).getPropertyValue('{property_name}')")
            assert current_property_value == property_value, \
                f'Actual property value: {current_property_value}, expected: {property_value}'

    def check_has_attribute(self, name: str, value: Pattern[str], nth: int = 0, **kwargs):
        step = f'Check that attribute "{name}" of "{self.name}" {self.type_of} matches pattern "{value.pattern}" '

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_attribute(name=name, value=value)

    def check_in_viewport(self, nth: int = 0, **kwargs):
        step = f'Check that the "{self.name}" {self.type_of} is in viewport'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_in_viewport()
