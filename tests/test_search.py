import allure


@allure.epic('Search')
class TestSearch:
    search_query = 'jeans'

    @allure.title('Can clear the search query in the search field')
    def test_clear_search_field(self, check, main_page):
        main_page.open()

        with check:
            main_page.navbar.check_placeholder_in_search_input()
        with check:
            main_page.navbar.enter_search_query(self.search_query)
            main_page.navbar.check_search_input_has_value(self.search_query)

            main_page.navbar.click_clear_search_field_btn()
            main_page.navbar.check_search_input_is_empty()

    @allure.title('Recent searches component appears after a search, has the relevant link and be cleared')
    def test_recent_searches(self, main_page, srp):
        main_page.open()

        main_page.navbar.enter_search_query(self.search_query)
        main_page.navbar.click_search_icon()
        srp.navbar.check_recent_searches_missing()

        srp.navbar.click_search_field()
        srp.navbar.check_recent_searches_present()
        srp.navbar.check_recent_searches_item_link(self.search_query)

        srp.navbar.click_clear_recent_searches_btn()
        srp.navbar.click_search_field()
        srp.navbar.check_recent_searches_missing()

    @allure.title('Check that the search query leads to relevant SRP')
    def test_positive_search(self, main_page, srp):
        main_page.open()

        main_page.navbar.enter_search_query(self.search_query)
        main_page.navbar.click_search_icon()

        srp.check_srp_url(self.search_query)
        srp.check_search_results_title_text(self.search_query)

    @allure.title('Check the No Results text for negative search')
    def test_negative_search(self, main_page, srp):
        search_query = '*'
        main_page.open()

        main_page.navbar.enter_search_query(search_query)
        main_page.navbar.click_search_icon()

        srp.check_srp_url(search_query)
        srp.check_no_results_header_text(search_query)
