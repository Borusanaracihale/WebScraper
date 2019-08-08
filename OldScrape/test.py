from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln
from elasticsearch import Elasticsearch
import json
import requests





es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
query = json.dumps({
"query": { 
"bool": { 
   "must": [
  { "match": { "uri":   "https://www.sahibinden.com/ilan/vasita-otomobil-ford-bayram-sekeri-hatasiz-boyasiz-degisensiz-718461519/detay" }} 
]
}
},
   "size":1
})





res = es.search(index="scrapelists",  body=query)

hit_id = res["hits"]["hits"][0]["_id"]

upt = es.update(index='scrapelists',doc_type='_doc',id=hit_id,body={"doc": {"isquery": True}})


print(upt)










'''
res =es.get(index='scrapesubmodels',doc_type='_doc',id = "https://www.sahibinden.com/daihatsu-yrv")
print(res)

if len(res["hits"]["hits"]) > 0 
    print("kayıt var")

print(res)



print(res["hits"]["hits"][0]["_source"]["uri"])


'''

'''
ureq = URLlib()

listings = IO.pickle_load('listings.pkl')

finlist = []

for itm in listings:
    if type(itm) == list:
        for j in itm:
            finlist.append(j)
    else:
        finlist.append(itm)

scr = DetailsScraper(finlist, 100, ureq, lowerdelay=1, upperdelay=2)
print("Scraping items from loaded listings...")
scr.scrapeDetails()
'''
