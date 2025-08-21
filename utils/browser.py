from logging import getLogger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # type:ignore

from constants.general_const import DEFAULT_TIMEZONE
from utils.config import Config

log = getLogger(__name__)


class Browser:
    def __init__(self, driver, global_timeout: int = None):
        self.driver = driver
        self.global_timeout = global_timeout  # Default global timeout in seconds

    @property
    def current_url(self) -> str:
        """
        Get the current URL of the browser.
        :return: current URL as a string
        """
        return self.driver.current_url

    def quit(self):
        """
        Close the browser and quit the WebDriver.
        """
        try:
            self.driver.quit()
        except Exception as e:
            log.error(f"Failed to quit browser: {e}")

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
        """
        Check if an element is present in the DOM by the given locator.
        :param by: locator strategy
        :param value: value of the locator
        :param expl_timeout: explicit wait timeout in seconds
        :return: bool indicating if the element is present
        """
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
        """
        Find an element by the given locator.
        :param by: locator strategy
        :param value: value of the locator
        :param expl_timeout: explicit wait timeout in seconds
        :return: WebElement objects if found, None otherwise
        """
        return WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
            EC.visibility_of_element_located((by, value)))

    def enter_text(self, by: str, value: str, text: str, expl_timeout=None) -> bool:
        """
        Enter text into field.
        :param by: locator strategy
        :param value: value of the locator
        :param text: text to enter
        :param expl_timeout: explicit wait timeout in seconds
        :return: True if text was entered successfully, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, expl_timeout or self.global_timeout).until(
                EC.visibility_of_element_located((by, value)))
            # clear field before entering text
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


def init_browser(config: Config) -> Browser:
    """
    Initialize a Browser instance with WebDriver.
    :param config: configuration object
    :return: Browser instance
    """
    width, height = config.screen_resolution.split("x")
    options = webdriver.ChromeOptions()
    # Arguments
    options.add_argument("--incognito")  # run in incognito mode
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--disable-dev-shm-usage")
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-save-password-bubble")

    # Snooze the "Change password" or "Save password" prompt
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    # Driver initialization (implemented only for Chrome browser)
    if config.remote_webdriver_url:
        options.set_capability("se:recordVideo", "true")
        options.set_capability("se:timeZone", DEFAULT_TIMEZONE)
        options.set_capability("se:screenResolution", f"{width}x{height}")
        options.set_capability("browserName", config.browser.lower())
        driver = webdriver.Remote(
            command_executor=config.remote_webdriver_url,
            keep_alive=True,
            options=options,
        )
    elif config.browser.lower() == 'chrome':
        config.remote_webdriver_url = None
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {'timezoneId': DEFAULT_TIMEZONE})
    elif config.browser.lower() == 'firefox':
        raise NotImplementedError("Firefox browser is not supported yet.")
    else:
        raise NotImplementedError(f"Unknown browser: {config.browser}")
    # set up IMPLICIT timeout if needed
    # driver.implicitly_wait(config.global_timeout)
    # Maximize the browser window if needed
    # driver.maximize_window()
    return Browser(driver=driver, global_timeout=config.global_timeout)
