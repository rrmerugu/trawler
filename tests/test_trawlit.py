from trawler import TrawlIt
import pytest


def test_scout():
    trawl = TrawlIt(kw="Ravi RT Merugu", max_pages=1)
    trawl.run()
    result = trawl.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    assert "search_kw" in result
    assert "search_kw_generated" in result


def test_scout_browser():
    
    with pytest.raises(NotImplementedError) as excinfo:
        trawl = TrawlIt(kw="Ravi RT Merugu", max_pages=1, browser="notbinga")
    assert "contact author for more info" in str(excinfo)
    
    
def test_keyword_generation():
    trawl = TrawlIt(kw="Django",  suffixes=['tutorials',], prefixes=['programming with',], generate_kws=True)
    assert 'programming with Django' in trawl.generated_keywords
    assert 'Django tutorials' in trawl.generated_keywords