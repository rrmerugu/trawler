from trawler.browsers.base import BrowserBase
from trawler.settings import DEFAULT_MAX_RESULTS_PER_PAGE, DEFAULT_MAX_PAGES
import json
import urllib


class BrowseBing(BrowserBase):
    """
    Does the browsing tasks on bing.com
    
    Usage:
        from trawler.browsers.bing import BrowseBing
        bing = BrowseBing(kw="invaana", max_page=3, source="en-us")
        bing.search()
        bing.data # returns the data
    
    """

    def __init__(self, kw=None, max_page=DEFAULT_MAX_PAGES, method='selenium-chrome', driver=None, **kwargs):
        SOURCE = kwargs.get('source', '')
        RESULTS_PER_PAGE = kwargs.get('pp', DEFAULT_MAX_RESULTS_PER_PAGE)
        super(BrowseBing, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

        self._BASE_URL = 'https://www.bing.com'
        self._SEARCH_QS = '/search?mkt={1}&count={2}&q='.format(self._BASE_URL, SOURCE, RESULTS_PER_PAGE)
        self._SEARCH_MAIN_CSS_SELECTOR = '.b_algo h2 a'
        self._SEARCH_KEYWORDS_CSS_SELECTOR = '.b_rs a'
        self._SEARCH_NEXT_QS = '&first='
        self._SEARCH_NEXT_CSS_SELECTOR = 'a.sb_pagN'
        self._DEFAULT_SCRAPE_METHOD = method
        self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + kw


class BrowseBingImages(BrowserBase):
    """
    Does the browsing tasks on bing.com

    Usage:
        from trawler.browsers.bing import BrowseBing
        bing = BrowseBing(kw="invaana", max_page=3, source="en-us")
        bing.search()
        bing.data # returns the data

    """

    def __init__(self, kw=None, max_page=DEFAULT_MAX_PAGES, method='selenium-chrome', driver=None, **kwargs):
        SOURCE = kwargs.get('source', '')
        RESULTS_PER_PAGE = kwargs.get('pp', DEFAULT_MAX_RESULTS_PER_PAGE)
        super(BrowseBingImages, self).__init__(kw=kw, max_page=max_page, method=method, driver=driver)

    def _get_image_results(self):
        images_list = []  # contains the link for Large original images, type of  image
        for i in range(self._ITER_MAX):
            url = "http://www.bing.com/images/search?q=" + self._SEARCH_TERM \
                  + "&FORM=HDRSC2&first={}&count=35&relp=35".format(i * 35)
            print(url)
            html = self.get_html(method=self._DEFAULT_SCRAPE_METHOD, url=url)
            soup = self._soup_data(html=html)

            for a in soup.find_all("a", {"class": "iusc"}):
                # print a
                mad = json.loads(a["mad"])
                source_url = mad["turl"]
                m = json.loads(a["m"])
                image_url = m["murl"]

                image_name = urllib.parse.urlsplit(image_url).path.split("/")[-1]
                image_data = {
                    "url": image_url,
                    "title": image_name,
                    "source_url": source_url
                }
                images_list.append(image_data)
        print(images_list)
        return images_list

    def get_image_results(self):
        return self._get_image_results()

    @property
    def data(self):
        images_result = self.get_image_results()
        data = {}
        data['webimage_result'] = images_result
        data['webimage_result_count'] = len(images_result)
        return data
