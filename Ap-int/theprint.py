import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import uuid
import hashlib
from datetime import datetime

## we can't add content extraction function in this website(theprint script), becouse we are getting irrelevant text 


website = "https://theprint.in/"
sub_categories = ["category/macrosutra/","category/diplomacy/","category/economy/","category/defence/","category/india/","category/ground-reports/","category/opinion/",""]


LINK_COLL=MongoClient()["edition_mv"]["data"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def theprint_data_collection(title,url,published_Date):
        hashURL = hashlib.md5(url.encode()).hexdigest()           
        if LINK_COLL.find_one({"hashurl":hashURL})==None:
                _id = str(uuid.uuid4())
                data_get={
                '_id':_id,    
                'Title':title,
                'Url':url,
                'Date':published_Date,
                'hashurl':hashURL,
                'domain_name':'theprint.in',
                'publisher_country':'India',
                'status':0,
                'language':None
                }
                print(data_get)
                LINK_COLL.insert_one(data_get)
 
def class_two_data(main_parent_class):
     if main_parent_class:
        parent_class_two = main_parent_class.find_all("div",class_="td-module-container td-category-pos-above")
        for elements in parent_class_two:
            title_tag = elements.find("h3",class_="entry-title td-module-title")
            title = title_tag.get_text(strip=True)  if title_tag else ''
            url_tag = title_tag.find("a")
            url = url_tag.get("href")
            date_element = elements.find("time",class_="entry-date updated td-module-date")
            published_Date = date_element.get_text(strip=True)  if date_element else ''
            theprint_data_collection(title,url,published_Date)
            

def theprint_class_one_data(main_parent_class):
    if main_parent_class:
        parent_class_one = main_parent_class.find("div",class_="td_block_inner tdb-block-inner td-fix-index")
        sub_parent_class = parent_class_one.find_all("div",class_="tdb_module_loop td_module_wrap td-animation-stack td-cpt-post")
        for elements in sub_parent_class:
            title_tag = elements.find("h3",class_="entry-title td-module-title")
            title = title_tag.get_text(strip=True)  if title_tag else ''
            url_tag = title_tag.find("a")
            url = url_tag.get("href")
            date_element = elements.find("time",class_="entry-date updated td-module-date")
            published_Date = date_element.text
            theprint_data_collection(title,url,published_Date)
           
    
def get_category_url(page_count):
    for sub_category in sub_categories:
       for page_number in range(1, page_count + 1):
            if page_number == 1:
                category_url = f"{website}{sub_category}"
            else:
                category_url = f"{website}{sub_category}page/{page_number}"
            print(category_url)
            response = requests.get(category_url,headers=headers)
            status  =response.status_code
            print("url_status_code==",status)
            soup = BeautifulSoup(response.content,"html.parser")
            main_parent_class = soup.find("div",class_="td-main-content-wrap td-container-wrap")
            class_two_data(main_parent_class)
            theprint_class_one_data(main_parent_class)
        

if __name__ =='__main__':
    page_count = 2
    get_category_url(page_count)
    
