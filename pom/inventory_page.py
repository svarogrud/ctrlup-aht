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


class InventoryPage:
    """Login page object model."""

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
        return Result(success=True, data=items_details, error_msg=None)
