import re

from pytest_bdd import when, then, parsers
from logging import getLogger

from utils.browser import Browser
from utils.result import Result

log = getLogger(__name__)


@when(parsers.re('I navigate to "(?P<url>.+)"'))
def step_navigate_to_url(browser: Browser, url: str):
    log.info(f'Navigating to "{url}"')
    assert browser.open_page(url), f'Failed to navigate to {url}, current URL is {browser.current_url}'


@when(parsers.re('log in using the following credentials:'))
def step_login(pages, datatable: list):
    result: Result = pages.login_page.is_page_opened()
    assert result.success, f'Login page not opened: {result.error_msg}'
    data = {row[0]: row[1] for row in datatable[1:]}
    result = pages.login_page.login(username=data.get("Username"), password=data.get('Password'), click_login=True)
    assert result.success, f'Failed to log in with credentials due to: {result.error_msg}'


# here items_num is parsed as an integer
@then(parsers.parse('inventory page displays exactly {items_num:d} items'))
def step_check_inventory_page_items(pages, items_num: int):
    # check page opened
    result: Result = pages.inventory_page.is_page_opened()
    assert result.success, f'Inventory page not opened: {result.error_msg}'

    # get inventory items
    result = pages.inventory_page.get_inventory_items()
    assert result.success, f'Failed to get inventory items: {result.error_msg}'
    assert len(result.data) == items_num, f'Expected {items_num} items, but found {len(result.data)} items'