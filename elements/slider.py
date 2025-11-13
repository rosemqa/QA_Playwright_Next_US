import allure
from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger('SLIDER')


class Slider(BaseElement):
    @property
    def type_of(self) -> str:
        return 'slider'

    def move_slider(self, offset_x=0, offset_y=0, nth: int = 0, **kwargs):
        step = f'Move "{self.name}" {self.type_of} handle by offset x={offset_x}, y={offset_y}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.drag_to(locator, target_position={"x": offset_x, "y": offset_y}, force=True)
