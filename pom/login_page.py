from selenium.webdriver.common.by import By

from utils.browser import Browser
from utils.result import Result


class ElementsMap:
    """A class to hold the locators for the login page elements."""
    is_page_opened = dict(by=By.CLASS_NAME, value='login_container')
    username_field = dict(by=By.XPATH, value='//input[@data-test="username"]')
    password_field = dict(by=By.ID, value='password')
    login_button = dict(by=By.ID, value='login-button')
    error = dict(by=By.XPATH, value='//h3[@data-test="error"]')


class LoginPage:
    """Login page object model."""

    def __init__(self, browser: Browser):
        self.browser = browser

    def is_page_opened(self, expl_timeout: int = 5) -> Result:
        """Check if the login page is opened."""
        present = self.browser.element_is_present(**ElementsMap.is_page_opened, expl_timeout=expl_timeout)
        return Result(
            success=present,
            error_msg=None if present else f"Login page is not detected by the locator: {ElementsMap.is_page_opened}"
        )

    def login(self,
              username: str = None,
              password: str = None,
              click_login: bool = True) -> Result:
        """Log in to the application using provided credentials.
        :param username: Username to log in with.
        :param password: Password to log in with.
        :param click_login: Whether to click the login button.
        :return: None if login is successful, or an error message if login fails.
        """
        if username and not self.browser.enter_text(**ElementsMap.username_field, text=username):
            return Result(error_msg="Failed to enter username")
        if password and not self.browser.enter_text(**ElementsMap.password_field, text=password):
            return Result(error_msg="Failed to enter password")
        if click_login and not self.browser.click_element(**ElementsMap.login_button):
            return Result(error_msg="Failed to click login button")

        if click_login and self.browser.element_is_present(**ElementsMap.error, expl_timeout=0.5):
            error = self.browser.get_text(**ElementsMap.error)
            return Result(success=not error, error_msg=error or None)
        return Result(success=True)
