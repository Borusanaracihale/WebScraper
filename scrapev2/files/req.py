from files.basescrape import URLrequests
import requests
#urllib requirements
import urllib
#urlsln requirements
from selenium import webdriver
import sys

class URLlib(URLrequests,object):
    def __init__(self,header,proxymain,res):
        super(URLlib,self).__init__()
        self.header=header
        self.proxymain=proxymain
        self.proxies = ""
        self.curretproxy = ""
        self.res = res
    def _readURL(self, url,use_proxy=False):        
        headers = self.header.getRandomChoiceHeader()
        if(use_proxy == True):
            self.proxies = self.proxymain.getProxies()
            for proxy in self.proxies:                
                try:
                    proxy = self.proxymain.getRandomProxy()
                    #request = urllib.request.Request(url, headers=headers,proxies=proxy)
                    request = requests.get(url,headers=headers,proxies=proxy,timeout=5)
                    
                    result = self.res.isSuccessRequest(request.content)
                    
                    print("Request State : " + str(result))
                    
                    if( result == True):
                        print("OK Proxy : " + str(proxy))
                        self.curretproxy = proxy
                        return result.content
                    else:
                        print("ERROR Proxy : " + str(proxy))                       
                        self.curretproxy = ""
                except:
                    print("EXCEPT Proxy : " + str(proxy) + " --- >  " + str(sys.exc_info()[0])) 
                    self.curretproxy = ""
                
            self.curretproxy = ""
            return ""            
        else:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                the_page = response.read()
                return the_page

class URLsln(URLrequests,object):
    def __init__(self):
        super(URLsln,self).__init__()
        ops = webdriver.ChromeOptions()
        ops.add_argument('headless')
        ops.add_argument('window-size=1400x900')
        self.driver = webdriver.Chrome(chrome_options=ops)

    def _readURL(self, url):
        self.driver.get(url)
        return self.driver.page_source

class URLreq(URLrequests,object):
    def __init__(self):
        super(URLreq,self).__init__()
        self.session = requests.Session()
    def _readURL(self, url):
        return requests.get(url).text

