import requests, os, re, time, random
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver


result = dict()
driver = webdriver.Chrome(os.getcwd() + "\chromedriver.exe")

def sleepRand(): 
    rand = random.random() * 1.5
    time.sleep(rand)

def scrapePage(pageUrl):
    url = pageUrl
    driver.get(url)
    
    time.sleep(5)

    html = driver.execute_script("return document.documentElement.innerHTML;")
    soup = bs(html, "html.parser")
    print(soup)

    ul = soup.find("ul", class_ = "petition_list")
    wraps = ul.find_all("div", class_ = "bl_wrap")

    for wrap in wraps:
        sleepRand()
        content = dict() 
        
        category = wrap.find("div", class_ = "bl_category ccategory cs wv_category").text
        category = re.search("분류 (.*)", category).group(1)

        title = wrap.find("div", class_ = "bl_subject").text
        title = re.search("제목 (.*)", title).group(1)
    
        href = wrap.find("a").get("href")
        href = "https://www1.president.go.kr/" + href

        result.update({href: [category, title, getText(href).strip()]})

    return len(wraps)

def getText(pageUrl):
    url = pageUrl
    driver.get(url)
    pageHtml = driver.page_source
    soup = bs(pageHtml, "html.parser")

    viewwrite = soup.find("div", class_ = "View_write")
    return viewwrite.text


for only in [1, 2]:
    url1 = "https://www1.president.go.kr/petitions/?c=46&only=" + str(only)
    page = 1
    
    while True:
        url2 = url1 + "&page=" + str(page) + "&order=1"
        print(url2)
        if scrapePage(url2) == 0:
            break
        page = page + 1



df = pd.DataFrame(result).transpose()
df.to_csv("result_petitions_animals.csv", header = False, index = False, encoding = 'utf-8-sig')
