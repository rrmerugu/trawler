from trawler.browsers import BrowseBing
from trawler.browsers.exceptions import BrowerScrapeMethodNotImplemented
import pytest


def test_browse_with_bing():
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=1)
    bing.search()
    result = bing.data
    bing.close()
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result


def test_browser_no_nextpage():
    bing = BrowseBing(kw="XxXXXXXXxxxxxbas dans dsand msad asd amd ansd am dna smda sdn asdmas dm", max_page=1)
    bing.search()
    result = bing.data
    bing.close()
    assert result['next_url'] is None


def test_browser_implamentation_error():
    bing = BrowseBing(kw="Hello", max_page=1, method="chrome")
    with pytest.raises(BrowerScrapeMethodNotImplemented) as excinfo:
        bing.search()
        bing.close()
    assert "Not implemented" in str(excinfo)
