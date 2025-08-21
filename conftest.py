import os
from logging import getLogger
from typing import Any, Generator

import pytest
import yaml
from pytest_bdd.parser import Step

from utils.apis import ApiCRUD, Api
from utils.browser import Browser, init_browser
from utils.config import Config
from utils.pages import Pages

log = getLogger(__name__)


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
    browser = init_browser(config)
    yield browser
    # Teardown
    browser.quit()


@pytest.fixture
def pages(browser, config: Config):
    """Get instance of Pages object with all page objects."""
    return Pages(browser)


@pytest.fixture
def api(config: Config) -> Api:
    """Get instance of API object with all services interfaces."""
    return Api(config)


def pytest_bdd_before_step_call(request,
                                feature,
                                scenario,
                                step: Step,
                                *_):  # noqa
    """Log current step start."""
    log.info(f'Starting step: "{step.name}"')
