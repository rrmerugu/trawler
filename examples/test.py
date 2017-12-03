import sys
sys.path.append('../')
from trawler.settings import DEFAULT_MAX_PAGES, DEFAULT_MAX_RESULTS_PER_PAGE
from trawler.browsers import BrowseBing

if __name__ == "__main__":
    max_page = 1
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=max_page, source="en-in")
    bing.search()
    result = bing.data
    print result, "+++++++++"
    assert bing.data['results_count'] != 0
    assert bing.data['results_count'] <= DEFAULT_MAX_RESULTS_PER_PAGE * max_page
    assert "selenium-htmlunit" == bing.shift_method()
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    # bing.close()
