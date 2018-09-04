# -*- coding: utf-8 -*-
import sys
import json

sys.path.append('../')
from trawler.trawl import TrawlIt, BrowseBingKeywords

if __name__ == "__main__":
    bing = BrowseBingKeywords(kw="machine learning",
                              method="requests",
                              extra_depth=True,
                              max_page=1,
                              )
    bing.run()
    result = bing.data

    with open('images_keywords.json', 'w') as fp:
        json.dump(str(result), fp)
