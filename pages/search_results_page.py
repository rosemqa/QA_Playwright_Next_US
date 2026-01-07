import re
from playwright.sync_api import Page
from components.navbar_component import NavbarComponent
from data.constants import Search
from data.links import URL
from elements.text import Text
from pages.base_page import BasePage


class SRP(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavbarComponent(page)

        self.search_results_title = Text(
            page, '[data-testid="plp-product-title-text"]', 'Search results title')
        self.no_results_header = Text(page, '[data-testid="plp-no-results-header"]', 'No results header')

    def check_search_results_title_text(self, title: str):
        self.search_results_title.check_have_text(text=f'"{title.upper()}"')

    def check_srp_url(self, search_query: str):
        self.check_current_url(re.compile(f'{URL.SRP}\\?w={search_query}'))

    def check_no_results_header_text(self, search_query: str):
        self.no_results_header.check_have_text(Search.NO_RESULTS_HEADER(search_query))
