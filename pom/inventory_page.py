from selenium.webdriver.common.by import By

from utils.browser import Browser
from utils.result import Result


class ElementsMap:
    """A class to hold the locators for the inventory page elements."""
    is_page_opened = dict(by=By.CLASS_NAME, value='inventory_container')
    items = dict(by=By.XPATH, value='//*[@data-test="inventory-item"]')
    item_name = dict(by=By.XPATH, value='.//*[@data-test="inventory-item-name"]')
    item_price = dict(by=By.XPATH, value='.//*[@data-test="inventory-item-price"]')
    item_desc = dict(by=By.XPATH, value='.//*[@data-test="inventory-item-desc"]')
    add_to_cart_button = dict(by=By.XPATH, value='.//button[text()="Add to cart"]')
    shopping_cart = dict(by=By.XPATH, value='//*[@data-test="shopping-cart-link"]')
    cart_badge = dict(by=By.XPATH, value='//*[@data-test="shopping-cart-badge"]')


class InventoryPage:
    """Inventory page object model."""

    def __init__(self, browser: Browser):
        self.browser = browser

    def is_page_opened(self, expl_timeout: int = 5) -> Result:
        """Check if the inventory page is opened."""
        present = self.browser.element_is_present(**ElementsMap.is_page_opened, expl_timeout=expl_timeout)
        return Result(
            success=present,
            error_msg=None if present else f"Inventory page is not detected by: {ElementsMap.is_page_opened}"
        )

    def get_inventory_items(self) -> Result:
        """Get inventory items.
        :return: Result object containing a list of inventory items if successful, or an error message if not.
        """
        # get items elements
        inventory_items = self.browser.find_elements(**ElementsMap.items)
        if not inventory_items:
            return Result(success=False, error_msg="No inventory items found")

        # get items details
        items_details = [
            {
                "name": item.find_element(**ElementsMap.item_name).text,
                "price": item.find_element(**ElementsMap.item_price).text,
                "description": item.find_element(**ElementsMap.item_desc).text,
            }
            for item in inventory_items
        ]
        return Result(success=True, data=items_details)

    def add_to_cart(self, item_index: int) -> Result:
        """Add an item to the shopping cart by its index.
        :param item_index: Index of the item to add (0-based).
        :return: Result object indicating success or failure.
        """
        items = self.browser.find_elements(**ElementsMap.items)
        if item_index >= len(items):
            return Result(error_msg=f"Item index {item_index} is out of range")

        error = None
        try:
            items[item_index].find_element(**ElementsMap.add_to_cart_button).click()
        except Exception as e:
            error = f"Failed to click 'Add to cart' button for item {item_index}: {str(e)}"
        return Result(success=not error, error_msg=error)

    def get_cart_badge_count(self) -> Result:
        """Get the count of items in the shopping cart badge.
        :return: Result object containing the badge count if successful, or an error message if not.
        """
        badge_count = None
        error = None
        # Check if the shopping cart badge is present
        if self.browser.element_is_present(**ElementsMap.shopping_cart):
            if self.browser.element_is_present(**ElementsMap.cart_badge):
                try:
                    badge_count = int(self.browser.get_text(**ElementsMap.cart_badge))
                except Exception as e:
                    error = f"Failed to get count of items in the cart badge: {e}"
            else:
                # No items in the cart, badge might not be present
                pass
        else:
            error = "Shopping cart is not present on the page"

        return Result(success=not error,
                      data=badge_count,
                      error_msg=error)
