import threading
from files.basescrape import Scraper, xpathSafeRead
from files.store import SQLStore
import time
import random


class MainScparer(Scraper,object):
    def __init__(self,n_jobs,uutils,header,proxies,response,lowerdelay=1,upperdelay=3,current_date="",main_url=""):
        super(MainScparer,self).__init__(url=main_url,njobs=n_jobs,lowerdelay=lowerdelay,upperdelay=upperdelay)
        self.brandList=[]
        self.modelList = []
        self.versionList =[]
        self.n_jobs = n_jobs
        self.uutils = uutils
        self.lock = threading.Lock()
        self.header=header
        self.url=main_url
        self.proxies = proxies
        self.response=response
        
    def getBrands(self):
        brandpage = self.uutils._readURL(self.url)
        self.response.crawlBrands(brandpage)
        
    def getModels(self):
        store = SQLStore()
        brandList= store.getBrands()
        for i in brandList:
            print(self.url + i[2])
            brand_page = self.uutils.delayedreadURL(self.url + i[2],self.lowerdelay,self.upperdelay)
            self.response.crawlModels(brand_page,i[0])
            
    def getVersions(self):
        store = SQLStore()
        modelList= store.getModels()
        for i in modelList:
            print(self.url + i[3])
            model_page = self.uutils.delayedreadURL(self.url + i[3],self.lowerdelay,self.upperdelay)
            self.response.crawlVersions(model_page,i[0])
            
    def getSubVersions(self):
        store = SQLStore()
        versionList = store.getVersions()
        for i in versionList:
            print(self.url + i[3])
            
            waittime = random.randint(2,8)
            
            print("Waiting " + str(waittime) + " sn.")
            time.sleep(waittime)
            version_page = self.uutils._readURL(self.url + i[3],False)
            self.response.crawlSubVersions(version_page,i[0])