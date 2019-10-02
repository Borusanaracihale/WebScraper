from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from files.basescrape import Scraper, xpathSafeRead

class Response(Scraper,object):
    def __init__(self,store):
        super(Response,self).__init__()
        self.store=store
        self.model_xpath = '//*[@id="searchCategoryContainer"]'
        self.error_xpath = '//*[@id="qr-error-footer"]/p/strong'
    def crawlBrands(self,response):
         soup = BeautifulSoup(response, 'html.parser')
         ctgList = soup.find_all("ul", {"class": "categoryList"})
         brandList = ctgList[0].find_all("li")
         
         storeList=[]
         
         for i in brandList:
             b_path = i.find("a", href=True)
             brand = {}
             brand["Name"] = b_path.text
             brand["Url"] = b_path["href"]
             storeList.append(brand)
             
         result = self.store.createBrands(storeList)
         print(result)
         
    def crawlModels(self,response,brand_id):
         soup = BeautifulSoup(response,'lxml')
         li_list = soup.find("div", id="searchCategoryContainer").select("ul > li")
         storeList=[]
         
         for i in li_list:
             b_path = i.find("a", href=True)
             model = {}
             model["BrandId"] = brand_id
             model["Name"] = b_path.text
             model["Url"] = b_path["href"]
             storeList.append(model)
             
         self.store.createModels(storeList)

         
    def crawlVersions(self,response,model_id):
         soup = BeautifulSoup(response,'lxml')
         li_list = soup.find("div", id="searchCategoryContainer").select("ul > li")
         storeList=[]
         
         for i in li_list:
             b_path = i.find("a", href=True)
             version = {}
             version["ModelId"] = model_id
             version["Name"] = b_path.text
             version["Url"] = b_path["href"]
             storeList.append(version)
          
         self.store.createVersions(storeList)
         

    def crawlSubVersions(self,response,version_id):
         soup = BeautifulSoup(response,'lxml')
         li_list = soup.find("div", id="searchCategoryContainer").select("ul > li")
         storeList=[]         
         if (len(li_list)  <= 0):
             version = self.store.getVersionById(version_id)
             for i in version:
                 sub_model = {}
                 sub_model["VersionId"] = version_id
                 sub_model["Name"] = i[2]
                 sub_model["Url"] = i[3]
                 storeList.append(sub_model)
         else:
             for i in li_list:
                 b_path = i.find("a", href=True)
                 sub_model = {}
                 sub_model["VersionId"] = version_id
                 sub_model["Name"] = b_path.text
                 sub_model["Url"] = b_path["href"]
                 storeList.append(sub_model)
             
         self.store.createSubVersions(storeList)

    def isSuccessRequest(self,response):
        c = response.content
        root = html.fromstring(c)
        err = {}
        err["result"] =  xpathSafeRead(root,self.error_xpath,'ERR.')
        
        if (err["result"] == "NA"):
            return True
        else:
            return False
        
         