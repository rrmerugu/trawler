from trawler.browsers import BrowseBing, BrowseStackOverFlow, BrowseStackOverFlowDocumentation
from trawler.browsers.exceptions import BrowerScrapeMethodNotImplemented
import pytest


def test_browse_with_bing():
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=1, method="requests")
    bing.search()
    result = bing.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()


def test_browse_with_bing_source_in():
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=1, method="requests", source="en-in")
    bing.search()
    result = bing.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()


def test_browse_with_bing_source_us():
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=1, method="requests", source="en-us")
    bing.search()
    result = bing.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    bing.close()


def test_browser_with_stackoverflow():
    stack = BrowseStackOverFlow(kw="Python Exception errors", max_page=1, method="requests")
    stack.search()
    result = stack.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    stack.close()


def test_browser_with_stackoverflow_doc():
    doc = BrowseStackOverFlowDocumentation(kw="django", method="requests")
    doc.search()
    result = doc.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    doc.close()
