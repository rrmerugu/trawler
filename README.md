# Invaana Trawler


[![Build Status](https://travis-ci.org/rrmerugu/trawler.svg?branch=master)](https://travis-ci.org/rrmerugu/trawler)
[![codecov](https://codecov.io/gh/rrmerugu/trawler/branch/master/graph/badge.svg)](https://codecov.io/gh/rrmerugu/trawler)


This is very light weight data gathering framework to search and gather information from web sources like Bing, 
Stackoverflow and etc. 

## Installation and Configuration

```bash

# install this package from PyPi
pip install trawler

# or for latest code
pip install git+https://github.com/rrmerugu/trawler.git#egg=trawler

# install selenium components including drivers (you need chrome installed in your machine)
npm install selenium-standalone@latest -g
selenium-standalone install # installs the drivers 
selenium-standalone start # starts the selenium server

pip install -r requirements/requirements.txt
```



## Usage


```python

from trawler import TrawlIt

trawl = TrawlIt(kw="MongoDB", generate_kws=True, browser="bing", method="requests")
#trawl = TrawlIt(kw="MongoDB", generate_kws=True, browser="bing")
trawl.run() # this will gather data from all generated keywords and saves it to MongoDB
trawl.generated_keywords # access the generated keywords ['learning MongoDB', 'Programming with MongoDB', 'MongoDB tutorials' ] 
trawl.data # access the data after the run
trawl.stop() # do this or there will be an idle browser instance left on your machine
# or 

trawl = TrawlIt(kw="Python Exception Error",  browser="stackoverflow")
trawl.run() # this will gather data and saves it to MongoDB
trawl.data # access the data after the run
trawl.stop() # do this or there will be an idle browser instance left on your machine



trawl = TrawlIt(kw="django",  browser="stackoverflow-doc")
trawl.run() # this will gather the topics from the stackoverflow documentation
trawl.data # access the data after the run
trawl.stop() # do this or there will be an idle browser instance left on your machine



trawl = TrawlIt(kw="django",  browser="wordpress")
trawl.run() # this will gather the topics from the stackoverflow documentation
trawl.data # access the data after the run
trawl.stop() # do this or there will be an idle browser instance left on your machine

from trawler.browsers.wordpress import BrowseWordPress
stack = BrowseWordPress( max_page=1, base_url="http://econbrowser.com/")
# stack = BrowseWordPress(kw="invaana", max_page=1, base_url="http://econbrowser.com")
stack.search()
stack.data # returns the data

```


## Supported Web sources

Current this framework supports, automating searches with 

- Bing
- Bing Images
- Bing Keywords
- StackOverFlow
- StackOverFlow Documentation
- Wordpress


## Important Note

Please understand https://advertise.bingads.microsoft.com/en-in/resources/policies/web-crawling before using this
framework. Make sure you comply with the respective website privacy policies before you crawl them.