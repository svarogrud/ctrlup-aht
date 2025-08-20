import os
from typing import Any, Generator

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from constants.general_const import DEFAULT_TIMEZONE
from utils.browser import Browser
from utils.config import Config
from utils.pages import Pages


def pytest_addoption(parser):
    parser.addoption("--cfg", action="store", dest="cfg", help="Environment config", required=False)


@pytest.fixture(scope="session")
def config(pytestconfig) -> Config:
    """Get config object with environment settings.
    :param pytestconfig: pytest config object.
    :return: Config object with environment settings.
    """
    config_file = pytestconfig.getoption("cfg")
    config_data = {}
    if config_file:
        file_path = os.path.join(
            os.path.dirname(__file__),
            'configs',
            config_file if config_file.endswith('.yml') else f"{config_file}.yml",
        )
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as cfg_data_file:
                config_data.update(yaml.load(cfg_data_file, Loader=yaml.SafeLoader))
    return Config(config_data)


@pytest.fixture
def browser(config: Config) -> Generator[Browser, Any, None]:
    """Get instance of Browser object with webdriver.
    :param config: config object
    """
    width, height = config.screen_resolution.split("x")
    options = webdriver.ChromeOptions()
    # Arguments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--disable-dev-shm-usage")
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")

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
    # set up IMPLICIT timeout
    driver.implicitly_wait(config.global_timeout)
    # Uncomment to maximize the browser window
    # driver.maximize_window()
    yield Browser(driver=driver, global_timeout=config.global_timeout)

    # Teardown
    driver.quit()


@pytest.fixture
def pages(browser, config: Config):
    """Get instance of Pages object with all pages."""
    return Pages(browser)
