from elements.base_element import BaseElement


class DropdownItem(BaseElement):
    @property
    def type_of(self) -> str:
        return 'dropdown_item'
