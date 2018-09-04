# -*- coding: utf-8 -*-
import sys
import json

sys.path.append('../')
from trawler.trawl import TrawlIt

if __name__ == "__main__":
    max_page = 1
    bing = TrawlIt(kw="Ravi RT Merugu",
                   method="requests",
                   max_page=max_page,
                   source="en-in",
                   generate_kws=True,
                   prefixes=['blogs of'],
                   suffixes=['blogs']
                   )
    bing.run()
    result = bing.data

    with open('data.json', 'w') as fp:
        json.dump(str(result), fp)
