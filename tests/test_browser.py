from trawler.browsers import BrowseBing, BrowseStackOverFlow, BrowseStackOverFlowDocumentation
from trawler.browsers.exceptions import BrowerScrapeMethodNotImplemented
import pytest
from trawler.settings import DEFAULT_MAX_RESULTS_PER_PAGE


def test_browse_with_bing():
    max_page = 1
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=max_page)
    bing.search()
    result = bing.data
    assert bing.data['results_count'] != 0
    assert bing.data[ 'results_count'] <= DEFAULT_MAX_RESULTS_PER_PAGE * max_page
    assert "selenium-htmlunit" == bing.shift_method()
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()


def test_browse_with_bing_source_enin():
    max_page = 2
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=max_page, source="en-in")
    bing.search()
    result = bing.data
    assert bing.data['results_count'] != 0
    assert bing.data['results_count'] <= DEFAULT_MAX_RESULTS_PER_PAGE * max_page
    assert "selenium-htmlunit" == bing.shift_method()
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()


def test_browse_with_bing_source_enus():
    max_page = 1
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=max_page, source="en-us")
    bing.search()
    result = bing.data
    assert bing.data['results_count'] != 0
    assert bing.data['results_count'] <= DEFAULT_MAX_RESULTS_PER_PAGE * max_page
    assert "selenium-htmlunit" == bing.shift_method()
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()



def test_browser_with_stackoverflow():
    stack = BrowseStackOverFlow(kw="Python Exception errors", max_page=1)
    stack.search()
    result = stack.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    stack.close()


def test_browser_with_stackoverflow_doc():
    doc = BrowseStackOverFlowDocumentation(kw="django")
    doc.search()
    result = doc.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    doc.close()


def test_browser_no_nextpage():
    bing = BrowseBing(kw="XxXXXXXXxxxxxbas dans dsand msad asd amd ansd am dna smda sdn asdmas dm", max_page=1)
    bing.search()
    result = bing.data
    assert result['next_url'] is None
    bing.close()


def test_browser_implamentation_error():
    with pytest.raises(BrowerScrapeMethodNotImplemented) as excinfo:
        bing = BrowseBing(kw="Hello", max_page=1, method="chromejjj")
        bing.search()
        bing.close()
    assert "Not implemented" in str(excinfo)
