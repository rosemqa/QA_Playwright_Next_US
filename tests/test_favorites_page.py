import allure


@allure.epic('Favorites page')
class TestFavoritesPage:
    @allure.title('Can add a product to cart from Favorites')
    def test_add_to_cart(self, check, add_to_favorites, fav_page):
        fav_page.open()
        product_name = fav_page.get_product_name()

        fav_page.click_size_dropdown()
        fav_page.select_random_size()
        fav_page.click_add_to_bag()

        with check:
            fav_page.check_moved_to_bag_notification_text(text=product_name)
            fav_page.check_moved_to_bag_notification_disappears()
        with check:
            fav_page.mini_cart.check_mini_cart_is_visible()
            fav_page.mini_cart.check_product_title_text(text=product_name)
        with check:
            fav_page.navbar.check_favorites_badge_is_inactive()
        with check:
            fav_page.navbar.check_cart_quantity(1)
        with check:
            fav_page.check_products_count(0)
        with check:
            fav_page.check_favorites_is_empty()

    @allure.title('Can not aad a product to cart without selecting the size')
    def test_add_to_cart_without_size(self, add_to_favorites, fav_page):
        fav_page.open()
        fav_page.check_size_dropdown_color('rgb(148, 148, 148)')

        fav_page.click_add_to_bag()
        fav_page.check_size_dropdown_color('rgb(217, 20, 64)')
        fav_page.navbar.check_cart_quantity(0)

    @allure.title('Can remove a product from Favorites')
    def test_remove_product(self, check, fav_page, add_to_favorites):
        fav_page.open()
        with check:
            fav_page.check_products_count(1)

        fav_page.click_remove_item()
        with check:
            fav_page.navbar.check_favorites_badge_is_inactive()
        with check:
            fav_page.check_products_count(0)
        with check:
            fav_page.check_favorites_is_empty()
