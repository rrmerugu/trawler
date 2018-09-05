from trawler.browsers import BrowseBing, BrowseBingImages, BrowseStackOverFlow, BrowseStackOverFlowDocumentation, \
    BrowseWordPress, BrowseBingKeywords
from trawler.browsers.utils import start_browser
from trawler.settings import AVAILABLE_METHODS, AVAILABLE_SELENIUM_METHODS
import logging

logger = logging.getLogger(__name__)


class TrawlIt(object):
    """
    This will run a browser search and returns the data with some extra operations on top
    of BrowseBing class

    USAGE:
        from trawler import TrawlIt

        trawl = TrawlIt(kw="MongoDB", generate_kws=True)
        trawl.generated_keywords # ['learning MongoDB', 'Programming with MongoDB', 'MongoDB tutorials' ]
        trawl.run() # this will gather data from all generated keywords and searches all
        trawl.stop()

        # or

        trawl = TrawlIt(kw="MongoDB")
        trawl.run() # this will gather data
        trawl.stop()


    """

    # _SUFFIXES = ['tutorials', ]
    # _PREFIXES = ['learning', 'Programming with']
    _AVAILABLE_BROWSERS = ['bing', 'bing-images','stackoverflow', 'stackoverflow-doc', ]
    _AVAILABLE_METHODS = AVAILABLE_METHODS

    def __init__(self, kw=None,
                 browser='bing',
                 max_pages=3,
                 method="selenium-chrome",
                 page_url=None,
                 generate_kws=False,
                 prefixes=None,
                 suffixes=None,
                 **kwargs):

        self._BASE_URL = page_url
        self._KEYWORD = kw
        self._BROWSER = browser
        self._SCRAPE_METHOD = method
        self._NOW_KEYWORD = kw
        self._MAX_PAGES = max_pages
        self._GENERATE_KWS = generate_kws
        self._GENERATED_KEYWORDS = []
        self._OTHER_KWARGS = kwargs
        self._DATA = {
            'generated_keywords_data': [],
            'generated_keywords': [],
            'search_keyword': None,
            'search_keyword_data': []

        }
        self._PREFIXES = prefixes if prefixes else []
        self._SUFFIXES = suffixes if suffixes else []

        if self._BROWSER not in self._AVAILABLE_BROWSERS:
            raise NotImplementedError("Only [%s] search is implemented at this moment, "
                                      "contact author for more info" % (",".join(self._AVAILABLE_BROWSERS)))

        if self._SCRAPE_METHOD in AVAILABLE_SELENIUM_METHODS:
            self._init_browser_instance()
        else:
            self._DRIVER = None

    @property
    def generated_keywords(self):
        # TODO - add generate keyword
        if len(self._GENERATED_KEYWORDS) == 0:
            if self._GENERATE_KWS:
                self._GENERATED_KEYWORDS = self._generate_keywords()
            else:
                self._GENERATED_KEYWORDS = [self._KEYWORD]
        return self._GENERATED_KEYWORDS

    @property
    def data(self):
        self._DATA['search_keyword'] = self._KEYWORD
        self._DATA['generated_keywords'] = self.generated_keywords
        if self._DATA['search_keyword_data'] is None:
            raise Exception("""Hey, either no results found or make sure you ran the code with `trawl.run()`
            
            Example:
                trawl = TrawlIt(kw=kw, generate_kws=True,  max_pages=10, browser="stackoverflow")
                trawl.run() # this will do the actual run
                trawl.data # you can access the data here
                trawl.stop() # this close the browser instance
            """)

        return self._DATA

    def _init_browser_instance(self):
        self._DRIVER = start_browser(self._SCRAPE_METHOD)

    def _generate_keywords(self):
        keywords = []
        for prefix in self._PREFIXES:
            keywords.append("%s %s" % (prefix, self._KEYWORD))

        for suffix in self._SUFFIXES:
            keywords.append("%s %s" % (self._KEYWORD, suffix))
        return keywords

    def _append_data(self, data):
        data['keyword'] = self._NOW_KEYWORD
        if "related_keywords" in data.keys():
            del data["related_keywords"]

        if self._NOW_KEYWORD == self._KEYWORD:
            self._DATA['search_keyword_data'] = data
        else:
            self._DATA['generated_keywords_data'].append(data)

        # self._DATA['search_keyword_data'].append(data)

        # self._DATA[self._NOW_KEYWORD]['results'] += data['results']
        # self._DATA[self._NOW_KEYWORD]['related_keywords'] += data['related_keywords']
        # self._DATA[self._NOW_KEYWORD]['related_keywords_count'] += data['related_keywords_count']
        # self._DATA[self._NOW_KEYWORD]['results_count'] += data['results_count']

    def _run(self, kw):

        source = self._OTHER_KWARGS.get('source')
        source_kwargs = {'source': source}
        if self._DRIVER:
            browser_kwargs = {'driver': self._DRIVER}
        else:
            browser_kwargs = {}

        extra_kwargs = {}
        extra_kwargs.update(browser_kwargs)
        if source:
            extra_kwargs.update(source_kwargs)
        if self._BROWSER == 'bing':
            browser = BrowseBing(kw=kw, max_page=self._MAX_PAGES, method=self._SCRAPE_METHOD,
                                 **browser_kwargs)
        elif self._BROWSER == 'bing-images':
            browser = BrowseBingImages(kw=kw, max_page=self._MAX_PAGES, method=self._SCRAPE_METHOD,
                                       **browser_kwargs)
        elif self._BROWSER == 'stackoverflow':
            browser = BrowseStackOverFlow(kw=kw, max_page=self._MAX_PAGES, method=self._SCRAPE_METHOD, **extra_kwargs)
        elif self._BROWSER == 'stackoverflow-doc':
            browser = BrowseStackOverFlowDocumentation(kw=kw, max_page=self._MAX_PAGES, method=self._SCRAPE_METHOD,
                                                       **extra_kwargs)
        elif self._BROWSER == 'wordpress':
            browser = BrowseWordPress(kw=kw, max_page=self._MAX_PAGES, base_url=self._BASE_URL,
                                      method=self._SCRAPE_METHOD, **extra_kwargs)

        browser.search()
        logger.debug("Gathered the data for keyword", kw)
        self._append_data(browser.data)

    def run(self):
        """
        Runs the data gathering jobs -
            **if self._GENERATE_KWS == True:** new keywords will be generated based on the prefixes, and suffixes is
            True, it will iterate through each keyword and gathers the information **else:** single keyword
            provided to the __init__() will be used and gathered data.

        :return:

        """
        if self._BROWSER == "bing-images":
            self._run(self._NOW_KEYWORD)
        else:
            self._GENERATED_KEYWORDS = self.generated_keywords
            if self._GENERATE_KWS:
                all_kws = list(set(self._GENERATED_KEYWORDS + [self._KEYWORD]))
                logger.debug("Generated %s keywords for [%s] " % (len(self._GENERATED_KEYWORDS), self._KEYWORD))
                for kw in all_kws:
                    self._NOW_KEYWORD = kw
                    self._run(self._NOW_KEYWORD)
            else:
                self._run(self._NOW_KEYWORD)

    def stop(self):
        if self._DRIVER:
            self._DRIVER.close()
