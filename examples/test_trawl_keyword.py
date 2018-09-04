# -*- coding: utf-8 -*-
import sys
import json

sys.path.append('../')
from trawler.trawl import TrawlIt, BrowseBingKeywords

if __name__ == "__main__":
    max_page = 5
    bing = BrowseBingKeywords(kw="machine learning",
                              method="requests",
                              )
    bing.run()
    result = bing.data

    with open('images_keywords.json', 'w') as fp:
        json.dump(str(result), fp)
