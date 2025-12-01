class PDP:
    SELECT_SIZE_ERROR = 'To continue, please complete your selection.'
    ACTIVE_ADD_TO_FAV_BTN_SRC = ('/static-content/ux-fabric/iconography-graphics/feature/next_revision/favourite-m'
                                 '-active.svg')
    INACTIVE_ADD_TO_FAV_BTN_SRC = ('/static-content/ux-fabric/iconography-graphics/feature/next_revision/favourite-m'
                                   '-default.svg')


class FavPage:
    NO_ITEMS = ("You have no saved items. Start to add your favourites by clicking the little heart next to items - "
                "we'll sync these across all your devices.")


class Bag:
    EMPTY_BAG = 'Your bag is empty'
    MOVED_TO_SFL = lambda product_name: f'{product_name} has been moved to Save For Later'
    MOVED_TO_BAG = 'Item has been moved to your bag'


class RecentlyViewed:
    empty_section = ('There are no Recently Viewed items to show. \n Items will appear here as you view them. You can '
                     'then select the images to revisit the items')
