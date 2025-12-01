from elements.base_element import BaseElement


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return 'input'
