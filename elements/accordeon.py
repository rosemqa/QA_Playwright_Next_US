from elements.base_element import BaseElement


class Accordion(BaseElement):
    @property
    def type_of(self) -> str:
        return 'accordion'
