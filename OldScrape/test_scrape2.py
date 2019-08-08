from s_scrape.base import Scraper, xpathSafeRead
from s_scrape.io import IO
import requests
# scraping
from bs4 import BeautifulSoup
from lxml import html
from elasticsearch import Elasticsearch
import re
import sys
import threading
import datetime
import json







es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#♫res=es.get(index='basescparedlist',doc_type='_doc',ilanno='715102637')

query = json.dumps({
        "query": {
                "match": {
                  "uri": {
                    "query": "https://www.sahibinden.com/daihatsu-yrv"
                  }
    },
   "size":"1"
  }
})



res = es.search(index="scrapesubmodels",  body=query)

print(res)


