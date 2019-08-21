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
dd=day

if day < 10:
    dd = "0"+ str(day)
    
if month < 10:
    mm = "0"+ str(month)
    
suffix = str(dd)+"-"+str(mm)+"-"+str(year)

listingswait = 5
mainwait = 15

ulib = URLlib()
ureq = URLreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(20, uutils=ulib, lowerdelay=3, upperdelay=3, current_date =suffix )
print("----------------------------Scraping Start----------------------------------------")
#last week = 7
print("---------------------Scraping Last 3 Days Start-----------------------------------")

print("Waiting %d seconds before scraping listings..." %mainwait)

#mscr.scrapeoffsetdayListings(3)

#links = []

#mscr.scrapeoffsetdayListingsinES(links)

print("---------------------Scraping Last 3 Days Finish---------------------------")


print("Waiting %d seconds before scraping listings..." %mainwait)


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
query = json.dumps({
                            "query": { 
                            "bool": { 
                               "must": [
                                          { "match": { "isquery":   False }} 
                                    ]
                                }
                            },
                            "size": 150000
                    })
                    
res = es.search(index="scrapelists",  body=query)

links = []

links = res['hits']['hits']

request_link = []

for mainlink in links:
    request_link.append(mainlink["_source"]["uri"])

print("Total Request : " + str(len(request_link)))

print("Waiting %d seconds before scraping listings..." %mainwait)

print("--------------------Scraping Links Start------------------------")

#time.sleep(mainwait)
scr = DetailsScraper(request_link, 15, ulib, lowerdelay=5, upperdelay=15,current_date =suffix)
print("Waiting %d seconds before scraping listings..." %mainwait)
#♣time.sleep(mainwait)
scr.scrapeDetails()

print("Waiting %d seconds before scraping listings..." %mainwait)

print("------------------------Scraping Finish---------------------------")




#IO.pickle_dump("listings_list.pkl", scr.final_list)
#print("--------------------------------finish-----------------------------------")
#print("Scraping & pickling complete.")
