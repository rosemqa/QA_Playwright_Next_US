import allure
from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger('IMAGE')


class Image(BaseElement):
    @property
    def type_of(self) -> str:
        return 'image'

    def get_image_source(self, nth: int = 0, **kwargs):
        step = f'Get source of {self.type_of} "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            return locator.get_attribute('src').split('?')[0]

    def check_image_source(self, source: str, nth: int = 0, **kwargs):
        step = f'Check source of {self.type_of} "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            image_src = locator.get_attribute('src').split('?')[0]
            assert image_src == source, f'Check image source, expected: {source}, actual: {image_src}'
