# -*- coding: utf-8 -*# scraping
from bs4 import BeautifulSoup
from lxml import html
from elasticsearch import Elasticsearch
import re
import sys
import threading

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class ElasticOperation():
    

    
    def getItem(index,key):
        es.
-

