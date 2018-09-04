# -*- coding: utf-8 -*-
import sys
import json

sys.path.append('../')
from trawler.trawl import TrawlIt, BrowseBingImages

if __name__ == "__main__":
    max_page = 5
    bing = BrowseBingImages(kw="machine learning",
                            method="requests",
                            max_page=max_page,
                            )
    bing.run()
    result = bing.data

    with open('images_data.json', 'w') as fp:
        json.dump(str(result), fp)
