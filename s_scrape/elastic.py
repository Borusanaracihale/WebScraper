# -*- coding: utf-8 -*# scraping
from bs4 import BeautifulSoup
from lxml import html
from elasticsearch import Elasticsearch
import re
import sys
import threading



class ElasticStore():
    def __init__(self):
        super(ElasticStore,self).__init__()
        self.es= Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
    
    def getSearch(self,index,query):
        res = self.es.search(index=index,  body=query)
        return res
    
    def createRow(self,index,query):
        res=self.es.index(index=index,doc_type='_doc',body=query)
        return res
    
    def updateRow(self,index,hit_id,query):
        self.es.update(index=index,doc_type='_doc',id=hit_id,body=query) 