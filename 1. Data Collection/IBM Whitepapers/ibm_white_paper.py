from bs4 import BeautifulSoup
import requests
import math
import os
import urllib.parse as encoder
import random
from datetime import date
import json
import re

#pdf.from_url('https://www.ibm.com/support/pages/node/6354911', '6354911.pdf')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def savePdfFile(soup, i):
    pdf_link = []
    try:
        for link in soup.find_all('a'):
            link = link['href']
            if(link.endswith(".pdf")):
                filename = os.path.basename(link)
                url = 'https://www.ibm.com' + encoder.quote(link)
                pdf_link.append(url)
                response = requests.get(url, headers=headers)
                #https://www.ibm.com/support/pages/system/files/inline-files/Integrating IBM zOS platform in CICD pipelines with GitLab - v1.7_1.pdf
                pdf = open("data/"+filename, 'wb')
                pdf.write(response.content)
                pdf.close()
    except:
        print("failed")
    return pdf_link

def parseDate(soup):
  for p in soup.find_all('p'):
    if "Modified date" in p.text:
      fs = p.text.strip().split("\n")
      return fs[len(fs) - 1].strip()
    
def today():
  today = date.today()
  return today.strftime("%d %B %Y")

def saveMetaData(filename, soup, url, attachment):
   metadata = {
      "title": filename,
      "publish_date": parseDate(soup),
      "extraction_date": today(),
      "url": url,
      "attachment": attachment
   }

   # Serializing json
   json_object = json.dumps(metadata, indent=4)
    
   # Writing to sample.json
   with open(f"data/{filename}.json", "w") as outfile:
    outfile.write(json_object)

def extractFileName(soup):
   for h1 in soup.find_all('h1', class_="ibm-northstart-content-page-title"):
      return h1.text.strip()
   
   return str(random.randint(999,9999))

page_size=100
first_page = 'https://www-api.ibm.com/search/api/v1/ibmcom/appid/dblue/responseFormat/json?query=&nr=10&sortby=-dcdate&scope=dblue&fr=20&rmdt=dcdate%2Cratings%2Csocialtags%2Cscope&disableGrouping=title_snippet&filter=(language:en%20AND%20(tsdoctype:DA900)%20AND%20(keywords:)%20AND%20(tsdoctype:DA900)%20AND%20(entitled:)%20AND%20(ibm_task_avl:WP)%20AND%20(dcdate:[19400109%20TO%2020230509]))'

result = requests.get(first_page)
json_result = result.json()
tatal_number_of_link = json_result['resultset']['searchresults']['totalresults']
total_page = math.ceil(tatal_number_of_link/page_size)
print("Page Size: ", page_size, ", Total article/blog: ", tatal_number_of_link, ", Total number of page: ", total_page)

page_from = 0
all_articles = []

## Collect all the articles and blog links from ibm api's
for page_number in range(1, total_page + 1):
    mainPage = f'https://www-api.ibm.com/search/api/v1/ibmcom/appid/dblue/responseFormat/json?query=&nr={page_size}&sortby=-dcdate&scope=dblue&fr={page_from}&rmdt=dcdate%2Cratings%2Csocialtags%2Cscope&disableGrouping=title_snippet&filter=(language:en%20AND%20(tsdoctype:DA900)%20AND%20(keywords:)%20AND%20(tsdoctype:DA900)%20AND%20(entitled:)%20AND%20(ibm_task_avl:WP)%20AND%20(dcdate:[19400109%20TO%2020230509]))'

    page_from = page_from + page_size

    result = requests.get(mainPage).json()

    link_list = result['resultset']['searchresults']['searchresultlist']
    
    for input_url in link_list:
        # trim ibm developer link
        parsed_link = input_url['url']
        all_articles.append(parsed_link)
        #print(parsed_link)

print("Total links: ", len(all_articles))



i = 0
for link in all_articles:
    rs = requests.get(link, headers=headers)
    soup = BeautifulSoup(rs.content, "html.parser")
    filename = extractFileName(soup)
    filename = re.sub(r'[\\/*?:"<>|]',"",filename)
    print(f"processing #{i}, #filename: {filename}, link: {link} ")
    with open(f"data/{filename}.html", "w", encoding = 'utf-8') as file:
        # prettify the soup object and convert it into a string
        file.write(str(soup.prettify()))
    
    pdf_link = savePdfFile(soup=soup, i=i)
    saveMetaData(filename=filename, soup=soup, attachment=pdf_link, url=link)
    
    i = i + 1
