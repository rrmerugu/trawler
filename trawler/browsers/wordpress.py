from trawler.browsers.base import BrowserBase


class BrowseWordPress(BrowserBase):
    """
    Does the browsing tasks on websites built on wordpress
    
    Usage:
        from trawler.browsers.wordpress import BrowseWordPress
        stack = BrowseWordPress( max_page=1, base_url="http://econbrowser.com/")
        # stack = BrowseWordPress(kw="invaana", max_page=1, base_url="http://econbrowser.com")
        stack.search()
        stack.data # returns the data
    
    """

    def __init__(self, kw=None, max_page=1, method='selenium-chrome', driver=None, base_url=None):
        super(BrowseWordPress, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        if base_url:
            self._BASE_URL = base_url
        self._BASE_URL = self._BASE_URL.strip('/')
        if self._BASE_URL is None:
            raise Exception(" Wordpress scraping methods need `base_url` \n "
                            "stack = BrowseWordPress(kw=\"invaana\", max_page=1, base_url=\"https://wordpress.com\")")
        self._SEARCH_QS = '/?s='
        self._SEARCH_MAIN_CSS_SELECTOR = '.entry-title a'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = None
        self._SEARCH_NEXT_QS = '/page/'
        self._SEARCH_NEXT_CSS_SELECTOR = '.nav-previous a'
        self._DEFAULT_SCRAPE_METHOD = method
        if kw:
            self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + kw
        else:
            self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS
