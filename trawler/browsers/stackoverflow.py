from .base import BrowserBase


class BrowseStackOverFlow(BrowserBase):
    """
    Does the browsing tasks on stackoverflow.com
    
    Usage:
        from trawler.browsers.stackoverflow import BrowseStackoverFlow
        stack = BrowseStackoverFlow(kw="invaana", max_page=1)
        stack.search()
        stack.data # returns the data
    
    """
    def __init__(self, kw=None, max_page=1, method=None, driver=None):
        super(BrowseStackOverFlow, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        self._BASE_URL = 'https://stackoverflow.com'
        self._SEARCH_QS = '/search?q='
        self._SEARCH_MAIN_CSS_SELECTOR = '.result-link a'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_QS = '&page='
        self._SEARCH_NEXT_CSS_SELECTOR = '.pager.fl a[rel="next"]'
        self._DEFAULT_SCRAPE_METHOD = "selenium"
