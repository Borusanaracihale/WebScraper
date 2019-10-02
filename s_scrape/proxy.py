
import requests
from lxml.html import fromstring
import random

class Proxies:
    def __init__(self,header):
        super(Proxies,self).__init__()
        self.header=header
        
    def getProxies(self):
        url = 'https://free-proxy-list.net/'
        headers = self.header.getRandomChoiceHeader()
        response = requests.get(url,headers=headers)
        parser = fromstring(response.text)
        proxies = []
        for i in parser.xpath('//tbody/tr')[:20]:
            #if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.append(proxy)
        return proxies
    
    def getRandomProxy(self):
        proxies = self.getProxies()
        proxy = random.choice(proxies)
        p = {"http": proxy, "https": proxy}
        return p
        
        