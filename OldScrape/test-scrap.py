# -*- coding: utf-8 -*-

from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln
from s_scrape.base import Scraper, xpathSafeRead

# scraping
from bs4 import BeautifulSoup
from lxml import html

import re
import sys
import threading

import time

ureq = URLlib()

finlist = []
finlist.append( "https://www.sahibinden.com/ilan/vasita-otomobil-audi-2012-audi-a1-1.6-tdi-s-tronic-cam-tavan-makyajli-anl-motors-711348598/detay")
finlist.append("https://www.sahibinden.com/ilan/vasita-otomobil-audi-75binde-kazasiz-boyasiz-audi-711057715/detay")
scr = DetailsScraper(finlist, 8, ureq, lowerdelay=2, upperdelay=5)
print("Scraping items from loaded listings...")
#scr.scrapeDetails()
results = scr.final_list
print(results)


    


car = {}
print("----> Using xpath for scraping from url:")
c = ureq.delayedreadURL(finlist[0], 2, 3)

root = html.fromstring(c)
car['ilanno'] = xpathSafeRead(root,'//*[@id="classifiedId"]', 'ilan.')
car['ilantarihi'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[2]/span', 'ilan tarihi.')
car['marka'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[3]/span', 'marka.')#root.xpath(self.marka_xpath)[0].text.strip()
car['seri'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[4]/span', 'seri.')
car['model'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[5]/span', 'model.')
car['yil'] = xpathSafeRead(root,  '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[6]/span', 'yil.')
car['yakit'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[7]/span', 'yakit.')
car['vites'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[8]/span', 'vites')
car['km'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[9]/span', 'km.')
car['motorgucu'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[11]/span', 'motor gucu.')
car['motorhacmi'] = xpathSafeRead(root,  '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[12]/span', 'motor hacmi.')
car['cekis'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[13]/span', 'cekis.')
# #car['Kapi'] = root.xpath(self.kapi_xpath)[0].text.strip() #kapi xpath not defined
car['renk'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[14]/span', 'renk.')
car['garanti'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[15]/span', 'garanti.')
car['plaka'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[16]/span', 'plaka/uyruk.')
car['kimden'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[17]/span', 'kimden.')
            
if(car['kimden'] == "Sahibinden"):
    car['owner'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[3]/div/div/div/h5', 'owner.')
else:
    car['owner'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/h5', 'owner.')
    

car['takas'] = xpathSafeRead(root, '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[18]/span', 'takas.')
car['durum'] = xpathSafeRead(root,  '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[19]/span', 'durumu.')
car['fiyat'] = xpathSafeRead(root,  '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h3', 'fiyat.')

print(car)


    

