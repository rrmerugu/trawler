from trawler.browsers.base import BrowserBase


class BrowseStackOverFlow(BrowserBase):
    """
    Does the browsing tasks on stackoverflow.com
    
    Usage:
        from trawler.browsers.stackoverflow import BrowseStackoverFlow
        stack = BrowseStackoverFlow(kw="invaana", max_page=1)
        stack.search()
        stack.data # returns the data
    
    """

    def __init__(self, kw=None, max_page=1, method='selenium-chrome', driver=None):
        super(BrowseStackOverFlow, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        self._BASE_URL = 'https://stackoverflow.com'
        self._SEARCH_QS = '/search?q='
        self._SEARCH_MAIN_CSS_SELECTOR = '.result-link a,.summary h3 a'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_QS = '&page='
        self._SEARCH_NEXT_CSS_SELECTOR = '.pager.fl a[rel="next"]'
        self._DEFAULT_SCRAPE_METHOD = method
        self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + kw


class BrowseStackOverFlowDocumentation(BrowserBase):
    def __init__(self, kw=None, max_page=1, method='selenium-chrome', driver=None):
        super(BrowseStackOverFlowDocumentation, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        self._BASE_URL = 'https://stackoverflow.com'
        self._SEARCH_QS = "/documentation/%s/topics/" % kw
        self._SEARCH_TERM = kw
        self._SEARCH_MAIN_CSS_SELECTOR = '.doc-topic-link'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_QS = '&page='
        self._SEARCH_NEXT_CSS_SELECTOR = '.pager a[rel="next"]'
        self._DEFAULT_SCRAPE_METHOD = method
        self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS
