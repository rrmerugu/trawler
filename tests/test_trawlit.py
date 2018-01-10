from trawler import TrawlIt
import pytest


def test_scout():
    trawl = TrawlIt(kw="Ravi RT Merugu", max_pages=1)
    trawl.run()
    result = trawl.data
    assert type(result) is dict
    assert "generated_keywords_data" in result
    assert "generated_keywords" in result
    assert "search_kw" in result
    assert "search_kw_data" in result
    assert "search_kw_generated" in result
    trawl.stop()


def test_scout_browser():
    
    with pytest.raises(NotImplementedError) as excinfo:
        trawl = TrawlIt(kw="Ravi RT Merugu", max_pages=1, browser="notbinga")
        trawl.stop()
    assert "contact author for more info" in str(excinfo)
    
    
def test_keyword_generation():
    trawl = TrawlIt(kw="Django",  suffixes=['tutorials',], prefixes=['programming with',], generate_kws=True)
    assert 'programming with Django' in trawl.generated_keywords
    assert 'Django tutorials' in trawl.generated_keywords
    trawl.stop()
