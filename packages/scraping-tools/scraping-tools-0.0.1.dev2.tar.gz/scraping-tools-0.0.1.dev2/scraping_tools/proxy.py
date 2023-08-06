import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from scraping_tools.logger import logger
from scraping_tools.driver import get_elem_by_css_selector, get_elem_by_class

PROXY_URL = "https://www.proxysite.com/"
SEARCH_CSS_SELECTOR = '#url-form-wrap > form > div.row > input[type="text"]'


def proxy(driver, url, timeout_seconds=30):
    """Use a proxy site to access required URLs.

    :param selenium.webdriver.remote.WebDriver driver: selenium webdriver instance.
    :param str url: the URL address to proxy to.
    :param number timeout_seconds: timeout in seconds.
    """
    logger.debug("Using proxy to get URL %r", url)
    driver.get(PROXY_URL)

    logger.debug("Getting servers drop down element")
    servers_drop_down = Select(
        get_elem_by_class(driver=driver,
                          class_name='server-option',
                          timeout_seconds=timeout_seconds)
    )
    selected_server = random.choice([option.text for option in servers_drop_down.options])

    logger.debug("Selecting a random server %s", selected_server)
    servers_drop_down.select_by_visible_text(selected_server)

    logger.debug("Getting search text box element")
    search_tb_elem = get_elem_by_css_selector(
        driver=driver,
        css_selector=SEARCH_CSS_SELECTOR,
        timeout_seconds=timeout_seconds
    )

    logger.debug("Clearing the search text box")
    search_tb_elem.clear()

    logger.debug("Sending url %r to text box", url)
    search_tb_elem.send_keys(url)

    logger.debug("Sending return key to text box")
    search_tb_elem.send_keys(Keys.RETURN)
