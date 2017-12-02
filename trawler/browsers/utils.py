import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def start_browser(scrape_method):
    if scrape_method == 'selenium-htmlunit':
        return webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)

    elif scrape_method == 'selenium-chrome':
        return webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME)

    else:
        raise Exception("Not implemented")
