from s_scrape.base import Scraper, xpathSafeRead
from s_scrape.io import IO

# scraping
from bs4 import BeautifulSoup
from lxml import html
from elasticsearch import Elasticsearch
import re
import sys
import threading
import json

class MainPageScraper(Scraper,object):
    def __init__(self, n_jobs, uutils, lowerdelay=1, upperdelay=5, current_date = "05-08-19"):
        super(MainPageScraper,self).__init__(url="https://www.sahibinden.com/kategori/otomobil", njobs = n_jobs, lowerdelay=lowerdelay, upperdelay=upperdelay)
        self._modelurls = []
        self.submodelurls = []
        self._listings = []
        self.n_jobs = n_jobs
        self.uutils = uutils
        self.lock = threading.Lock()
        self._current_date = current_date
        
    @property
    def linklist(self):
        return self._modelurls

    @property
    def listings(self):
        return self._listings
    

    
    #Private methods
    def _get_submodels_from_page(self, url, url_delayed=True):
        sublist = list()
        print("----> Scraping sub-models from url: %s" % (url))
        if url_delayed:
            c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
        else:
            c = self.uutils.readURL(url)
        soup = BeautifulSoup(c, "html.parser")
        subList = soup.find_all("li", {"class": "cl3"})

        
        for itm in subList:
            tmp = itm.find("a", href=True)
            if tmp['href'] != "#":
                ret_str = "https://www.sahibinden.com" + tmp['href']
                uri = {}
                uri["uri"]  = ret_str
                uri ["isquery"] = False
                uri["addeddate"] = self._current_date
                es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                res=es.index(index='scrapesubmodels',doc_type='_doc',body=uri)
        return sublist
    

    def _get_listings_from_page(self, url, url_delayed=True):
        if url is None:
            pass
        try:
            print("----> Scraping listings from url: %s" % (url))
            if url_delayed:
                c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
            else:
                c = self.uutils.readURL(url)
            soup = BeautifulSoup(c, "html.parser")
            listitems = soup.find_all("tr", {"class": "searchResultsItem"})

            for i in range(len(listitems)):
                try:
                    cur = listitems[i]
                    a_curr = cur.a
                    print('Link posting: ' + a_curr['href'])
                    ret_str = "https://www.sahibinden.com" + a_curr['href']
                    self.lock.acquire()
                    self._listings.append(ret_str)                    
                    tmpLink = {}
                    tmpLink["uri"] = ret_str
                    tmpLink["isquery"] = False
                    tmpLink["addeddate"] = self._current_date
                    tmpLink["ilanno"] = listitems[i]["data-id"]
                    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                    query = json.dumps({
                            "query": { 
                            "bool": { 
                               "must": [
                                          { "match": { "uri":   ret_str }} 
                                    ]
                                }
                            },
                           "size":1
                    })
                    
                    res = es.search(index="scrapelists",  body=query)
                    
                    if res["_shards"]["successful"] == 1:
                        result_count = len(res["hits"]["hits"])
                        if len(result_count) > 0:
                             if res["hits"]["hits"][0]["_source"]["uri"] == ret_str:
                                 continue
                    
                  
                    res=es.index(index='scrapelists',doc_type='_doc',body=tmpLink)
                    print("result list add :" + ret_str)
                    self.lock.release()
                except:
                    self.lock.release()
                    print('Read error in: ' + str(i))

            return listings_list

        except:
            pass


    def _get_listings_from_page_last_week(self, url, url_delayed=True):
        if url is None:
            pass
        try:
            if url_delayed:
                c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
            else:
                c = self.uutils.readURL(url)
            soup = BeautifulSoup(c, "html.parser")
            listitems = soup.find_all("tr", {"class": "searchResultsItem"})
            
            if len(listitems) > 0:
                es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                for i in range(len(listitems)):
                    try:
                        cur = listitems[i]
                        a_curr = cur.a
                        ret_str = "https://www.sahibinden.com" + a_curr['href']
                        self.lock.acquire()
                        self._listings.append(ret_str)                    
                        tmpLink = {}
                        tmpLink["uri"] = ret_str
                        tmpLink["isquery"] = False
                        tmpLink["addeddate"] = self._current_date
                        tmpLink["addeddate"] = self._current_date
                        tmpLink["ilanno"] = cur["data-id"]
                        print(tmpLink)
                        query = json.dumps({
                                "query": { 
                                "bool": { 
                                   "must": [
                                              { "match": { "uri":   ret_str }} 
                                        ]
                                    }
                                },
                               "size":1
                        })
                        
                        print("Add url : " + ret_str)
                        res = es.search(index="scrapelists",  body=query)
                        
                        if res["_shards"]["successful"] == 1:
                            result_count = len(res["hits"]["hits"])
                            if result_count > 0:
                                 if res["hits"]["hits"][0]["_source"]["uri"] == ret_str:
                                         print("Is Exist : " + ret_str)
                                         self.lock.release()
                                         continue
                    
                    
                        res=es.index(index='scrapelists',doc_type='_doc',body=tmpLink)  
                        print("Added url : " + ret_str)
                        self.lock.release()
                    except:
                        print('Read error in: ' + str(i))
                        continue

        except:
            pass

    def _get_listings_upperlimit(self, link):
        try:
            c = self.uutils.readURL(link)
            xpth = '//*[@id="searchResultsSearchForm"]/div/div[4]/div[1]/div[2]/div/div[1]/span'

            tot = self.uutils.choosebyXPath(c, xpth)
            tot = tot.replace(".", "")
            tot = re.findall('\d+',tot)
            tot = int(tot[0])
            rem = tot % 20
            tot = tot + rem
            if tot < 20:
                tot = 20
            return min(tot, 980)
        except:
           print("Read error - upperlimit: " + link)
           return 20
       
    

    def _wrapperBatchRun_upperlimits(self):
 
        query = json.dumps({
               "query" : {
                "match_all" : {}
            },
            "size": 1000
        })
    
        flat_list = []
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        res = es.search(index="scrapesubmodels",  body=query)
        
        flat_list = res['hits']['hits']
        links = []
        for mainlink in flat_list:
            if mainlink is None:
                continue
            else:
                upperlimit = self._get_listings_upperlimit(mainlink["_source"]["uri"])
                print("Upperlimit for link: %s   -->   is %s" % (mainlink["_source"]["uri"], str(upperlimit)))
                for pagingoffset in range(0, upperlimit + 10, 20):
                    link = mainlink["_source"]["uri"] + "?pagingOffset=" + str(pagingoffset)
                    links.append(link)
                    tmpLink = {}
                    tmpLink["uri"] = link
                    tmpLink["isquery"] = False
                    tmpLink["addeddate"] = self._current_date
                    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                    res=es.index(index='scrapeupperlimitlinks',doc_type='_doc',body=tmpLink)
        return links

    def _wrapperBatchRun_upperlimitslastweek(self,day):
 
        #flat_list = IO.flatten_list(self.submodelurls)
        
        query = json.dumps({
               "query" : {
                "match_all" : {}
            },
            "size": 1000
        })
    
        flat_list = []
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        res = es.search(index="scrapesubmodels",  body=query)
        
        flat_list = res['hits']['hits']
        links = []
        for mainlink in flat_list:
            if mainlink is None:
                continue
            else:
                
                page_uri = mainlink["_source"]["uri"] + "?date="+str(day)+"day"
                
                if day != 1:
                    page_uri = page_uri + "s"
                
                upperlimit = self._get_listings_upperlimit(page_uri)
                print("Upperlimit for link: %s   -->   is %s" % (page_uri, str(upperlimit)))
                for pagingoffset in range(0, upperlimit + 10, 20):
                    link = page_uri + "&pagingOffset=" + str(pagingoffset)
                    tmpLink = {}
                    tmpLink["uri"] = link
                    tmpLink["isquery"] = False
                    tmpLink["addeddate"] = self._current_date
                    
                    
                    query = json.dumps({
                                "query": { 
                                "bool": { 
                                   "must": [
                                              { "match": { "uri":   link }} 
                                        ]
                                    }
                                },
                               "size":1
                        })
                        
                    res = es.search(index="scrapeupperlimitlastweeklinks",  body=query)
                    
                    #already add links
                    links.append(link)
                    
                    if res["_shards"]["successful"] == 1:
                            result_count = len(res["hits"]["hits"])
                            if result_count > 0:
                                 if res["hits"]["hits"][0]["_source"]["uri"] == link:
                                         print("Exist Upper Link: " + link)
                                         continue
                    
                    
                    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                    res=es.index(index='scrapeupperlimitlastweeklinks',doc_type='_doc',body=tmpLink)
                    print("Added Upper Link : " + link)
        return links

    def _wrapperBatchRun_appendlistings(self, url):
        self._get_listings_from_page(url)
        
    def _wrapperBatchRun_appendlistingslastweek(self, url):
        self._get_listings_from_page_last_week(url)

    def _wrapperBatchRun_scrapeModels(self, car):
        tmp = car.find("a", href=True)
        uri = "https://www.sahibinden.com" + tmp['href'] + "?pagingOffset="
        self._modelurls.append(uri)
        print(self._current_date)
        tmpUri = {}
        tmpUri["uri"] = uri
        tmpUri["isquery"] = False
        tmpUri["addeddate"] = self._current_date
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        res=es.index(index='scrapemodels',doc_type='_doc',body=tmpUri)
    #Public methods
    def scrapeModels(self):
        c = self.uutils.readURL(self.link)
        soup = BeautifulSoup(c, "html.parser")
        ctgList = soup.find_all("ul", {"class": "categoryList"})
        carList = ctgList[0].find_all("li")        
        self.batchrun(self._wrapperBatchRun_scrapeModels, carList)

    def _wrapperBatchRun_scrapeSubModels(self,url):
        self.submodelurls.append(self._get_submodels_from_page(url))
        
        
    def scrapeSubModels(self):
        self.batchrun(self._wrapperBatchRun_scrapeSubModels, self._modelurls)

    def scrapeListings(self):
        links = self._wrapperBatchRun_upperlimits()
        self.batchrun(self._wrapperBatchRun_appendlistings,links)

    def scrapeoffsetdayListings(self,day):
        links = self._wrapperBatchRun_upperlimitslastweek(day)
        self.batchrun(self._wrapperBatchRun_appendlistingslastweek,links)
        
    def scrapeoffsetdayListingsinES(self,links):
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        query = json.dumps({
                                    "query": { 
                                    "bool": { 
                                       "must": [
                                                 { "match": { "uri":  "3days" }}
                                            ]
                                        }
                                    },
                                    "size": 10000
                            })
                            
        res = es.search(index="scrapeupperlimitlastweeklinks",  body=query)
        
        links = []
        
        links = res['hits']['hits']
        
        request_link = []
        
        for mainlink in links:
            request_link.append(mainlink["_source"]["uri"])
            
        self.batchrun(self._wrapperBatchRun_appendlistingslastweek,request_link)
        
class DetailsScraper(Scraper):
    def __init__(self, listings, n_jobs, uutils, lowerdelay=1, upperdelay=6,current_date = ""):
        super().__init__(url="", njobs=n_jobs, lowerdelay=lowerdelay, upperdelay=5)
        self.listings = listings
        self.final_list = []
        self.n_jobs = n_jobs
        self.uutils=uutils
        self._current_date = current_date
        #Xpath references for posting details
        self.ilan_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[1]/span'
        self.ilantarihi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[2]/span'
        self.marka_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[3]/span'
        self.seri_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[4]/span'
        self.model_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[5]/span'
        self.yil_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[6]/span'
        self.yakit_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[7]/span'
        self.vites_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[8]/span'
        self.km_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[9]/span'
        self.kasatipi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[10]/span'
        self.motorgucu_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[11]/span'
        self.motorhacmi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[12]/span'
        self.cekis_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[13]/span'
        self.renk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[14]/span'
        self.garanti_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[15]/span'
        self.plakauyruk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[16]/span'
        self.kimden_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[17]/span'
        self.takas_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[18]/span'
        self.durum_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[19]/span'
        #self.durum_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[20]/span'
        self.galeri_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/h5'
        self.sahibinden_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[3]/div/div/div/h5'
        self.fiyat_xpath =      '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h3'
        self.il_xpath =      '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h2/a'
        self.container_xpath = '//*[@id="classifiedDetail"]'

    def _get_details_from_url_xpath(self, url):

        car = {}
        store = {}
        c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
        try:
            root = html.fromstring(c)
 
            car['ilanno'] = xpathSafeRead(root, self.ilan_xpath, 'ilan.')
            car['ilantarihi'] = xpathSafeRead(root, self.ilantarihi_xpath, 'ilan tarihi.')
            car['sehir'] = xpathSafeRead(root, self.il_xpath, 'sehir.')
            car['marka'] = xpathSafeRead(root, self.marka_xpath, 'marka.')
            car['seri'] = xpathSafeRead(root, self.seri_xpath, 'seri.')
            car['model'] = xpathSafeRead(root, self.model_xpath, 'model.')
            car['yil'] = xpathSafeRead(root, self.yil_xpath, 'yil.')
            car['yakit'] = xpathSafeRead(root, self.yakit_xpath, 'yakit.')
            car['vites'] = xpathSafeRead(root, self.vites_xpath, 'vites')
            car['km'] = xpathSafeRead(root, self.km_xpath, 'km.')
            car['kasatipi'] = xpathSafeRead(root, self.kasatipi_xpath, 'kasa tipi.')
            car['motorgucu'] = xpathSafeRead(root, self.motorgucu_xpath, 'motor gucu.')
            car['motorhacmi'] = xpathSafeRead(root, self.motorhacmi_xpath, 'motor hacmi.')
            car['cekis'] = xpathSafeRead(root, self.cekis_xpath, 'cekis.')
            car['renk'] = xpathSafeRead(root, self.renk_xpath, 'renk.')
            car['garanti'] = xpathSafeRead(root, self.garanti_xpath, 'garanti.')
            #car['hasardurumu'] = xpathSafeRead(root, self.hasar_xpath, 'hasar durumu.')
            car['plaka'] = xpathSafeRead(root, self.plakauyruk_xpath, 'plaka/uyruk.')
            car['kimden'] = xpathSafeRead(root, self.kimden_xpath, 'kimden.')
            
            if(car['kimden'] == "Sahibinden"):
                car['owner'] = xpathSafeRead(root, self.sahibinden_xpath, 'owner.')
            else:
                car['owner'] = xpathSafeRead(root, self.galeri_xpath, 'owner.')
            
            car['takas'] = xpathSafeRead(root, self.takas_xpath, 'takas.')
            car['durum'] = xpathSafeRead(root, self.durum_xpath, 'durumu.')
            car['fiyat'] = xpathSafeRead(root, self.fiyat_xpath, 'fiyat.')
            car['uri'] = url
            #car['path'] = c
            car['is_riding'] = 1
            car['addeddate'] = self._current_date
            
           
            es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
            
            '''
            store["ilanno"] = car["ilanno"]
            store["html"] = c
            
            result_store = es.index(index='htmlstore',doc_type='_doc',body=store)
            '''
            result = es.index(index='basescparedlist',doc_type='_doc',body=car)
            
            query = json.dumps({
                            "query": { 
                            "bool": { 
                               "must": [
                                          { "match": { "uri":   url }} 
                                    ]
                                }
                            },
                           "size":1
                    })
                    
            search_res = es.search(index="scrapelists",  body=query)
            hit_id = search_res["hits"]["hits"][0]["_id"]
            upt = es.update(index='scrapelists',doc_type='_doc',id=hit_id,body={"doc": {"isquery": True}})
            
            print(" **** Processing complete ****  --------> " + car['ilanno'] )
            return car
        except:
            print(sys.exc_info()[0], " occured.")


    def _wrapperBatchRun(self, url):
        car = self._get_details_from_url_xpath(url)
        self.final_list.append(car)


    def scrapeDetails(self):
        self.batchrun(self._wrapperBatchRun, self.listings)

