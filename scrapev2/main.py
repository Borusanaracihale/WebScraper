from files.header import MainHeader
from files.res import Response
from files.proxy import Proxies
from files.req import URLlib
from files.store import SQLStore
from files.scrapingmain import MainScparer
import datetime


store= SQLStore()
header = MainHeader()
response = Response(store)
proxy = Proxies(header)
ulib = URLlib(header,proxy,response)

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


mainscrape = MainScparer(10,ulib,header,proxy,response,2,4,suffix,"https://www.sahibinden.com")

#first work
#mainscrape.getBrands()
#mainscrape.getModels()
#mainscrape.getVersions()
mainscrape.getSubVersions()






