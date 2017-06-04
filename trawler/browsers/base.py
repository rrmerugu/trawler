import selenium.webdriver as webdriver
import lxml
import lxml.html
from . import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging


class BrowserBase(object):
    """
    Base class for making new browser classes like BingBrowser, GoogleBrowser, DuckDuckGoBrowser etc
    
    
    USAGE:
        _BASE_URL : https://www.bing.com # this should be changed for each Child class
        _PHANTOMJS_PATH : #phantomjs binary path
        _DEFAULT_METHOD : #default method used to scrape ? selenium or python requests
        
    """

    def __init__(self, kw=None, max_page=None, method=None, driver=None):
        """
        Make some quick calculations to proceed with the run
        """

        self._AVAILABLE_SCRAPE_METHODS = ['selenium']
        self._DEFAULT_SCRAPE_METHOD = self._AVAILABLE_SCRAPE_METHODS[0]

        self._BASE_URL = None
        self._SEARCH_QS = None
        self._SEARCH_TERM = None
        self._SEARCH_URL = None

        self._HTML_DATA = None
        self._SOUPED_HTML_DATA = None

        self._RESULTS_MAIN = []
        self._RESULTS_KEYWORDS = []

        self._SEARCH_MAIN_CSS_SELECTOR = None
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_CSS_SELECTOR = None

        self._NEXT_PAGE_URL = None

        self._ITER = 0
        self._ITER_MAX = 3
        
        self._SEARCH_TERM = kw
        
        if max_page:
            self._ITER_MAX = max_page
            
        if method:
            self._DEFAULT_SCRAPE_METHOD = method

        if driver is None:
            self._init_browser_instance()
        else:
            self._DRIVER = driver

    def _test_config(self):
        """
        this will check the inputs and executables being in place
        :return:
        """
        logging.debug('testing config')
    
    def _soup_data(self):
         return lxml.html.fromstring(self._HTML_DATA)
    
    def _init_browser_instance(self):
        self._DRIVER = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME)
    
    def get_html_selenium(self):
        """
        https://stackoverflow.com/a/18102579/3448851
        :return:
        """
        if self._NEXT_PAGE_URL:
            self._DRIVER.get(self._NEXT_PAGE_URL)
        else:
            self._DRIVER.get(self._SEARCH_URL)
        return self._DRIVER.page_source
        
    def get_html(self, method=None):
        if method is None:  method = self.get_current_method()
        print "909090090900", method
        if method == 'selenium':  return self.get_html_selenium()
        else: raise exceptions.BrowerScrapeMethodNotImplemented('Not implemented')
        
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
        self._DEFAULT_SCRAPE_METHOD = self._AVAILABLE_SCRAPE_METHODS[index+1]
    
    def search(self):
        """
         1. Perform a dry run
         2. shift _DEFAULT_SCRAPE_METHOD if needed
         3. get results
         """
        if self._ITER == 0:
            self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + self._SEARCH_TERM
        self.dry_run()
        self._test_config()
        self._HTML_DATA = self.get_html()
        self._SOUPED_HTML_DATA = self._soup_data()
        self._RESULTS_MAIN += self.get_search_results()
        self._RESULTS_KEYWORDS += self.get_related_keywords()
        self._NEXT_PAGE_URL = self._get_next_page()
        
        if self._NEXT_PAGE_URL and self._ITER < self._ITER_MAX:
            self._ITER += 1
            self.search()
        
    @property
    def data(self):
        # make the data unique
        self._RESULTS_MAIN = [dict(y) for y in set(tuple(x.items()) for x in self._RESULTS_MAIN)]
        self._RESULTS_KEYWORDS = [dict(y) for y in set(tuple(x.items()) for x in self._RESULTS_KEYWORDS)]
        return {
            'results': self._RESULTS_MAIN ,
            'results_count': len(self._RESULTS_MAIN),
            'related_keywords': self._RESULTS_KEYWORDS,
            'related_keywords_count': len(self._RESULTS_KEYWORDS),
            'next_url': self._NEXT_PAGE_URL
        }

    def _scrape_css_selector(self, selector=None):
        results = self._SOUPED_HTML_DATA.cssselect(selector)
        data = []
        for result in results:
            link =  result.get('href').strip() if result.get('href') else None
            datum = {
                'link': link if link.startswith('http') else self._BASE_URL + link,
                'text': result.text_content().strip() if result.text_content() else None
            }
            data.append(datum)
        return data
    
    def _get_next_page(self):
        """
        :return:
        """
        if self._SEARCH_NEXT_CSS_SELECTOR:
            el = self._SOUPED_HTML_DATA.cssselect(self._SEARCH_NEXT_CSS_SELECTOR)
            if len(el) >= 1:
                el = el[0]
                return self._BASE_URL + el.get('href').strip()
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
        self._DRIVER.close()
