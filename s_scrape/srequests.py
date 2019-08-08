from s_scrape.base import URLrequests
from s_scrape.api import routed

from lxml.html import fromstring
import requests
from itertools import cycle
#urllib requirements
import urllib
import random

#urlsln requirements
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class URLlib(URLrequests,object):
    def __init__(self):
        super(URLlib,self).__init__()
        self.user_agent_list = [
                # Chrome
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (X11; Linuxlistings =  x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                # Firefox
                'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
            ]




    def _readURL(self, url):
        
        random_user_agent = random.choice(self.user_agent_list)
        headers = {'User-Agent': random_user_agent}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            the_page = response.read()
        return the_page
        '''
        url_proxy = "https://free-proxy-list.net/"
        random_user_agent = random.choice(self.user_agent_list)
        headers = {'User-Agent': random_user_agent}
        response = requests.get(url_proxy,headers=headers)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
                
        proxy_pool = cycle(proxies)
        for i in range(1,len(proxies) + 1):
            try:
                 print("Request : " + str(i))
                 proxy = next(proxy_pool)
                 response = requests.get(url,headers=headers,proxies={"http": proxy, "https": proxy})
                 return response.content
                 break
            except:
                 print("Skipping. Connnection error")
        '''

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

class APIreq(URLrequests,object):
    def __init__(self):
        super(APIreq,self).__init__(bypassdelayed=True)
    def _readURL(self, url):
        try:
            return routed(url)
        except:
            print("!Failed requesting from api, using urllib!")
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            return response.read()
