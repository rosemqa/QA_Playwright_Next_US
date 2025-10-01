import pytest

from pages.main_page import MainPage


class BaseTest:
    main_page = MainPage

    @pytest.fixture()
    def setup(self, request, page):
        request.cls.main_page = MainPage(page)
        # self.main_page = MainPage(page)

