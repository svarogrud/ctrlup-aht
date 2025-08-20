from logging import getLogger

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # type:ignore

log = getLogger(__name__)


class Browser:
    def __init__(self, driver, global_timeout: int = 5):
        self.driver = driver
        self.global_timeout = global_timeout  # Default global timeout in seconds

    @property
    def current_url(self):
        return self.driver.current_url

    def open_page(self, url: str) -> bool:
        """
        Open a web page in the browser.
        :param url: URL of the page to open
        :return: True if the page was opened successfully, False otherwise
        """
        try:
            self.driver.get(url)
            return self.driver.current_url.strip('/') == url.strip('/')
        except Exception as e:
            log.error(f"Failed to open page {url}: {e}")
        return False

    def element_is_present(self, by: str, value: str, expl_timeout=None) -> bool:
        try:
            return bool(WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.presence_of_element_located((by, value))))
        except Exception as e:
            log.debug(f"Element not found by {by}='{value}': {e}")
        return False

    def find_elements(self, by: str, value: str, expl_timeout=None) -> list[WebElement]:
        """
        Find elements by the given locator.
        :param by: locator strategy
        :param value: value of the locator
        :param expl_timeout: explicit wait timeout in seconds
        :return: list of WebElement objects if found, empty list otherwise
        """
        try:
            return WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.presence_of_all_elements_located((by, value)))
        except Exception as e:
            log.debug(f"Failed to find elements by {by}='{value}': {e}")
        return []

    def find_element(self, by: str, value: str, expl_timeout=None) -> WebElement:
        return WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
            EC.visibility_of_element_located((by, value)))

    def enter_text(self, by: str, value: str, text: str, expl_timeout=None) -> bool:
        """
        Enter text into an input field.
        :param by: locator strategy
        :param value: value of the locator
        :param text: text to enter
        :param expl_timeout: explicit wait timeout in seconds
        :return: True if text was entered successfully, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            log.debug(f"Failed to enter text '{text}' in element by {by}='{value}': {e}")
        return False

    def get_text(self, by: str, value: str, expl_timeout=None) -> str:
        """
        Get text from an element found by the given locator.
        :param by: locator strategy
        :param value: value of the locator
        :param expl_timeout: explicit wait timeout in seconds
        :return: text of the element if found, empty string otherwise
        """
        try:
            element = WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.visibility_of_element_located((by, value)))
            return element.text
        except Exception as e:
            log.debug(f"Failed to get text from element by {by}='{value}': {e}")
        return ""

    def click_element(self, by: str, value: str, expl_timeout=None) -> bool:
        """
        Click an element identified by the given locator.
        :param by: locator strategy
        :param value: value of the locator
        :param expl_timeout: explicit wait timeout in seconds
        :return: True if the element was clicked successfully, False otherwise
        """
        try:
            WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.element_to_be_clickable((by, value))).click()
            return True
        except Exception as e:
            log.debug(f"Failed to click element by {by}='{value}': {e}")
        return False
