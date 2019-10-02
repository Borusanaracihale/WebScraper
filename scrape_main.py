from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln
from s_scrape.header import MainHeader
from s_scrape.elastic import ElasticStore
from s_scrape.proxy import Proxies
import datetime
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
mainwait = 5

ulib = URLlib()
ureq = URLreq()
header = MainHeader()
proxy = Proxies(header)
elastic = ElasticStore()


#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(40, uutils=ulib,header=header,proxy=proxy,elastic=elastic, lowerdelay=2, upperdelay=5, current_date =suffix ,is_riding=0)
print("----------------------------Scraping Start----------------------------------------")
#last week = 7
print("---------------------Scraping Last 3 Days Start-----------------------------------")

print("Waiting %d seconds before scraping listings..." %mainwait)


#mscr.scrapeModels()
#mscr.scrapeSubModels()
#mscr.scrapeListings()
#mscr.scrapeoffsetdayListings(3)

links = []

#mscr.scrapeoffsetdayListingsinES(links)

print("---------------------Scraping Last 3 Days Finish---------------------------")

print("Waiting %d seconds before scraping listings..." %mainwait)

query = json.dumps({
                            "query": { 
                            "bool": { 
                                    
                               "must": [
                                          { "match": { "isquery":   False }} 
                                    ]
                                }
                            },
                            "size": 15
                    })
                    

res = elastic.getSearch('scrapelists',query)

links = []

links = res['hits']['hits']

request_link = []

for mainlink in links:
    request_link.append(mainlink["_source"]["uri"])

print("Total Request : " + str(len(request_link)))

print("Waiting %d seconds before scraping listings..." %mainwait)

print("--------------------Scraping Links Start------------------------")

#time.sleep(mainwait)
scr = DetailsScraper(request_link, 200, ulib,header=header,proxy=proxy,elastic=elastic, lowerdelay=2, upperdelay=4,current_date =suffix)
print("Waiting %d seconds before scraping listings..." %mainwait)
#♣time.sleep(mainwait)
scr.scrapeDetails()

print("Waiting %d seconds before scraping listings..." %mainwait)

print("------------------------Scraping Finish---------------------------")




#IO.pickle_dump("listings_list.pkl", scr.final_list)
#print("--------------------------------finish-----------------------------------")
#print("Scraping & pickling complete.")
