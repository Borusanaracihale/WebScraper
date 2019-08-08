from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln
import time
import datetime
from elasticsearch import Elasticsearch
import json

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year


if day < 10:
    dd = "0"+ str(day)
    
if month < 10:
    mm = "0"+ str(month)
    
suffix = str(dd)+"-"+str(mm)+"-"+str(year)

listingswait = 5
mainwait = 30

ulib = URLlib()
ureq = URLreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(20, uutils=ulib, lowerdelay=3, upperdelay=3, current_date =suffix )
print("Scraping started...")
#mscr.scrapeModels()
#print("Main car models scraped...")size:
#mscr.scrapeSubModels()
#print("Sub car models scraped...")
#print("Waiting %d seconds before scraping listings..." %listingswait)
#mscr.scrapeListings()

#last week = 7
#mscr.scrapeoffsetdayListings(7)

'''
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
query = json.dumps({
                            "query": { 
                            "bool": { 
                               "must": [
                                          { "match": { "isquery":   False }} 
                                    ]
                                }
                            },
                            "size": 5000
                    })
                    
res = es.search(index="scrapeupperlimitlastweeklinks",  body=query)

links = []

links = res['hits']['hits']

request_link = []



for mainlink in links:
    request_link.append(mainlink["_source"]["uri"])

print(len(request_link))

mscr.scrapeoffsetdayListingsinES(request_link)
print("--------------------------------------Finish-------------------------------------------------")
'''
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
query = json.dumps({
                            "query": { 
                            "bool": { 
                               "must": [
                                          { "match": { "isquery":   False }} 
                                    ]
                                }
                            },
                            "size": 50000
                    })
                    
res = es.search(index="scrapelists",  body=query)

links = []

links = res['hits']['hits']

request_link = []

for mainlink in links:
    request_link.append(mainlink["_source"]["uri"])

print(len(request_link))
#time.sleep(mainwait)
scr = DetailsScraper(request_link, 15, ulib, lowerdelay=7, upperdelay=15,current_date =suffix)
print("Waiting %d seconds before scraping listings..." %mainwait)
#♣time.sleep(mainwait)
scr.scrapeDetails()
print("--------------------------------------Finish-------------------------------------------------")




#IO.pickle_dump("listings_list.pkl", scr.final_list)
#print("--------------------------------finish-----------------------------------")
#print("Scraping & pickling complete.")
