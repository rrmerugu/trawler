from .base import BrowserBase


class BrowseBing(BrowserBase):
    """
    Does the browsing tasks on bing.com
    
    Usage:
        from trawler.browsers.bing import BrowseBing
        bing = BrowseBing(kw="invaana", max_page=3)
        bing.search()
        bing.data # returns the data
    
    """
    def __init__(self, kw=None, max_page=3, method='selenium-chrome', driver=None):
        super(BrowseBing, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        self._BASE_URL = 'https://www.bing.com'
        self._SEARCH_QS = '/search?q='
        self._SEARCH_MAIN_CSS_SELECTOR = '.b_algo h2 a'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = '.b_rs a'
        self._SEARCH_NEXT_QS = '&first='
        self._SEARCH_NEXT_CSS_SELECTOR = 'a.sb_pagN'
        self._DEFAULT_SCRAPE_METHOD = method
        self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + kw
