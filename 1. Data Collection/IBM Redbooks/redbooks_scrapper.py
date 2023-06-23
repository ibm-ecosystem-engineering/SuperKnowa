import os
from bs4 import BeautifulSoup
import requests
import math
import sys


corpus_folder ="/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/redbooks_data"
def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

first_page="https://www.redbooks.ibm.com/xml/rbutf8.xml"

result = requests.get(first_page)
#print(result.content)
#json_result = result.json()
soup = BeautifulSoup(result.content, features="xml")
list = soup.find_all('IBMRedbooksDoc')

file_data_list =[]
for data in list:
    pub_date = data.find('PubDate').text
    last_updated = data.find('LastUpdate').text
    url = data.find('URL').text
    pdf_url = data.find('PDFURL').text
    print(pub_date)
    file_name = os.path.basename(pdf_url)
    meta_data_file = corpus_folder+"/"+file_name.replace(".pdf",".json")
    downloadFile(pdf_url,corpus_folder+"/"+file_name)

    print(meta_data_file)

    with open(meta_data_file, "+w") as fp1:
            fp1.write("URL: "+str(url))
            fp1.write("\n")
            fp1.write("updated_date: "+str(last_updated))
            fp1.write("\n")
            fp1.write("publish_date: "+str(pub_date))
            fp1.write("\n")
            fp1.write("file_name: "+str(file_name))
            fp1.write("\n")
    print("metadata file created succesfully")



