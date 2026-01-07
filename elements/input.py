import allure
from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger('INPUT')


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return 'input'

    def fill(self, value: str, nth: int = 0, **kwargs):
        step = f'Fill {self.type_of} "{self.name}" with value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.fill(value)

    def check_has_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Check that {self.type_of} "{self.name}" has value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.fill(value)
