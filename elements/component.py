from elements.base_element import BaseElement


class Component(BaseElement):
    @property
    def type_of(self) -> str:
        return 'component'
