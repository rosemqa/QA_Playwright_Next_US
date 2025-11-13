from elements.base_element import BaseElement


class Checkbox(BaseElement):
    @property
    def type_of(self) -> str:
        return 'checkbox'
