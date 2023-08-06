import contextlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from scraping_tools.logger import logger


@contextlib.contextmanager
def driver_session():
    """Web-driver session context manager.

     - Create a web driver.
     - Yields the driver
     - Quit & cleanup when done.
    """
    logger.debug("Creating a web-driver session")

    driver = webdriver.Remote(
        command_executor='http://phantomjs:8910',
        desired_capabilities=DesiredCapabilities.PHANTOMJS
    )

    driver.maximize_window()
    driver.set_window_position(0, 0)
    driver.implicitly_wait(30)

    try:
        yield driver
    except:
        logger.exception("Session encountered an unexpected error")
        raise
    finally:
        logger.debug("Session quitting web-driver")
        driver.close()
        driver.quit()


def get_elem_by_xpath(driver, xpath, timeout_seconds=30):
    """Return an element by xpath."""
    return wait_for_element(driver, xpath, By.XPATH, timeout=timeout_seconds)


def get_elem_by_class(driver, class_name, timeout_seconds=30):
    """Return an element by class name."""
    return wait_for_element(driver, class_name, By.CLASS_NAME, timeout=timeout_seconds)


def get_elem_by_css_selector(driver, css_selector, timeout_seconds=30):
    """Return an element by css selector."""
    return wait_for_element(driver, css_selector, By.CSS_SELECTOR, timeout=timeout_seconds)


def wait_for_element(driver, identifier, by=By.ID, timeout=30):
    """Return an element once it's located."""
    return WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, identifier)))


def wait_for_clickable_element(driver, identifier, by=By.ID, timeout=30):
    """Return an element once it's located and clickable."""
    return WebDriverWait(driver, timeout).until(ec.element_to_be_clickable((by, identifier)))
