from elements.base_element import BaseElement


class Dropdown(BaseElement):
    @property
    def type_of(self) -> str:
        return 'dropdown'
