from pom.inventory_page import InventoryPage
from pom.login_page import LoginPage


class Pages:
    """Container for all page objects."""

    def __init__(self, browser):
        self.browser = browser
        # Initialize page objects on first request
        self.__login_page = None
        self.__inventory_page = None

    @property
    def login_page(self):
        """Get the login page object."""
        if not self.__login_page:
            self.__login_page = LoginPage(self.browser)
        return self.__login_page

    @property
    def inventory_page(self):
        """Get the inventory page object."""
        if not self.__inventory_page:
            self.__inventory_page = InventoryPage(self.browser)
        return self.__inventory_page
