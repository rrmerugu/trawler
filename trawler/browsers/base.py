from bs4 import BeautifulSoup
import requests
from trawler.browsers import exceptions
from trawler.browsers.utils import start_browser
import logging
import random, time
from trawler.settings import AVAILABLE_METHODS, DEFAULT_MAX_PAGES
from user_agent import generate_user_agent
from datetime import datetime

logging.getLogger(__name__)


class BrowserBase(object):
    """
    Base class for making new browser classes like BingBrowser, GoogleBrowser, DuckDuckGoBrowser etc
    
    
    USAGE:
        _BASE_URL : https://www.bing.com # this should be changed for each Child class
        _PHANTOMJS_PATH : #phantomjs binary path
        _DEFAULT_METHOD : #default method used to scrape ? selenium-chrome or selenium-htmlunit
        
    """

    def __init__(self, kw=None, max_page=None, method='selenium-chrome', driver=None):
        """
        Make some quick calculations to proceed with the run
        """

        self._AVAILABLE_SCRAPE_METHODS = AVAILABLE_METHODS

        self._BASE_URL = None
        self._SEARCH_QS = None
        self._SEARCH_TERM = None
        self._SEARCH_URL = self._BASE_URL
        if self._SEARCH_QS: self._SEARCH_URL = self._SEARCH_URL + self._SEARCH_QS
        if self._SEARCH_TERM: self._SEARCH_URL = self._SEARCH_URL + self._SEARCH_TERM
        self._PAUSE_RUN_RANDOMLY = lambda: random.randint(1, 4)

        self._HTML_DATA = None
        self._SOUPED_HTML_DATA = None

        self._RESULTS_MAIN = []
        self._RESULTS_KEYWORDS = []

        self._SEARCH_MAIN_CSS_SELECTOR = None
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_CSS_SELECTOR = None

        self._NEXT_PAGE_URL = None

        self._ITER = 0
        self._ITER_MAX = DEFAULT_MAX_PAGES

        self._SEARCH_TERM = kw

        if max_page:
            self._ITER_MAX = max_page

        self._DEFAULT_SCRAPE_METHOD = method
        if self._DEFAULT_SCRAPE_METHOD in ['selenium-htmlunit', 'selenium-chrome', ]:
            if driver is None:
                self._init_browser_instance()
            else:
                self._DRIVER = driver
        else:
            self._DRIVER = None

        if self._DEFAULT_SCRAPE_METHOD not in self._AVAILABLE_SCRAPE_METHODS:
            raise exceptions.BrowerScrapeMethodNotImplemented('Not implemented')

    def _test_config(self):
        """
        this will check the inputs and executables being in place
        :return:
        """
        logging.debug('testing config')

    def _soup_data(self, html=None):
        # return lxml.html.fromstring(self._HTML_DATA)
        if html is None:
            html = self._HTML_DATA
        return BeautifulSoup(html, "lxml")

    def _init_browser_instance(self):
        self._DRIVER = start_browser(self._DEFAULT_SCRAPE_METHOD)

    def evaluate_url(self):
        """
        decide which url to scrape now
        :return:
        """
        if self._NEXT_PAGE_URL:
            return self._NEXT_PAGE_URL
        else:
            return self._SEARCH_URL

    def get_html_with_selenium(self, url=None):
        """
        scrapes the html content using requests module

        https://stackoverflow.com/a/18102579/3448851
        :return:
        """
        if url is None:
            url = self.evaluate_url()
        self._DRIVER.get(url)
        return self._DRIVER.page_source

    def get_headers(self):
        return generate_user_agent()

    def get_html_with_requests(self, url=None):
        """
        scrapes the html content using requests module
        :return:
        """
        if url is None:
            url = self.evaluate_url()

        headers = {"User-Agent": self.get_headers()}
        try:
            req = requests.get(url, timeout=10, headers=headers)
            if req.status_code == 200:
                return req.text
            else:
                return None
        except Exception as e:
            return None

    def get_html(self, method=None, url=None):
        if method is None:  method = self.get_current_method()
        if method in ['selenium-htmlunit', 'selenium-chrome', ]: return self.get_html_with_selenium(url=url)
        if method == 'requests': return self.get_html_with_requests(url=url)

    def dry_run(self):
        """
        This will run a dry run with plain python requests, and check if requests is good enough,
        and if there is some issue, the driver will be switched to Selenium
        :return:
        """
        pass

    def get_current_method(self):
        """
        Returns the current Browser driver being used by this class (requests or selenium)
        :return:
        """
        return self._DEFAULT_SCRAPE_METHOD

    def shift_method(self):
        """
        swaps the current method to other method. If python requests is current method, it will shift to next one, which is
        selenium
        :return:
        """
        index = self._AVAILABLE_SCRAPE_METHODS.index(self._DEFAULT_SCRAPE_METHOD)
        return self._AVAILABLE_SCRAPE_METHODS[index - 1]

    def search(self):
        for i in range(self._ITER_MAX):
            logging.debug(self._NEXT_PAGE_URL, self._ITER, self._ITER_MAX, "======")
            if i == 0 or self._NEXT_PAGE_URL:
                self._ITER += 1
                time.sleep(self._PAUSE_RUN_RANDOMLY())
                self.search_single_page(i)

    def search_single_page(self, iter_num=0):
        """
         1. Perform a dry run
         2. shift _DEFAULT_SCRAPE_METHOD if needed
         3. get results
         """

        self.dry_run()
        self._test_config()
        self._HTML_DATA = self.get_html()
        self._SOUPED_HTML_DATA = self._soup_data()
        self._RESULTS_MAIN += self.get_search_results()
        self._RESULTS_KEYWORDS += self.get_related_keywords()
        self._NEXT_PAGE_URL = self._get_next_page()

    @property
    def data(self):
        # make the data unique
        self._RESULTS_MAIN = [dict(y) for y in set(tuple(x.items()) for x in self._RESULTS_MAIN)]
        self._RESULTS_KEYWORDS = [dict(y) for y in set(tuple(x.items()) for x in self._RESULTS_KEYWORDS)]

        data = {
            'result': self._RESULTS_MAIN,
            'result_count': len(self._RESULTS_MAIN),

            'related_keywords': self._RESULTS_KEYWORDS,
            'next_url': self._NEXT_PAGE_URL,
            'crawled_at': datetime.now()

        }
        return data

    def _scrape_css_selector(self, selector=None):
        results = self._SOUPED_HTML_DATA.select(selector)
        data = []
        for result in results:
            link = result.get('href').strip() if result.get('href') else None
            datum = {
                'url': link if link.startswith('http') else self._BASE_URL + link,
                'text': result.getText().strip() if result.getText() else None
            }
            data.append(datum)
        return data

    def _get_next_page(self):
        """
        :return:
        """
        if self._SEARCH_NEXT_CSS_SELECTOR:
            el = self._SOUPED_HTML_DATA.select(self._SEARCH_NEXT_CSS_SELECTOR)
            if len(el) >= 1:
                el = el[0]
                href = el.get('href').strip()
                if "http://" in href or "https://" in href:
                    return href
                return self._BASE_URL + href
        else:
            return None

    def get_search_results(self):
        return self._scrape_css_selector(self._SEARCH_MAIN_CSS_SELECTOR)

    def get_related_keywords(self):
        if self._SEARCH_KEYWORDS_CSS_SELECTOR:
            return self._scrape_css_selector(self._SEARCH_KEYWORDS_CSS_SELECTOR)
        else:
            return []

    def close(self):
        if self._DRIVER:
            self._DRIVER.close()
