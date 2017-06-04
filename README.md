# Invaana Trawler


[![Build Status](https://travis-ci.org/invaana/trawler.svg?branch=master)](https://travis-ci.org/invaana/trawler)
[![codecov](https://codecov.io/gh/invaana/trawler/branch/master/graph/badge.svg)](https://codecov.io/gh/invaana/trawler)


This is very light weight data gathering framework to search and gather information from sites like Bing, 
Stackoverflow and etc. 

## Installation and Configuration

```bash
# install this package with pip
pip install -e  git+https://github.com/invaana/trawler.git#egg=trawler

# install selenium components including drivers (you need chrome installed in your machine)
npm install selenium-standalone@latest -g
selenium-standalone install # installs the drivers 
selenium-standalone start # starts the selenium server

pip install -r requirements/requirements.txt
```



## Usage


```python

from trawler import TrawlIt

scout = TrawlIt(kw="MongoDB", generate_kws=True, save=False)
scout.generated_keywords # ['learning MongoDB', 'Programming with MongoDB', 'MongoDB tutorials' ] 
scout.run() # this will gather data from all generated keywords and saves it to MongoDB

# or 

scout = TrawlIt(kw="MongoDB")
scout.run() # this will gather data and saves it to MongoDB


```