from bs4 import BeautifulSoup
import requests
import math
import pandas as pd
import numpy as np
from time import sleep
import re

page_size=100
first_page = 'https://www.ibm.com/docs/api/v1/products/all'
result = requests.get(first_page)

json_result = result.json()

def remove_extra_lines(data):
    data =re.sub(r'\n\s*\n', '\n', data, flags=re.MULTILINE)
    return data

def pre_processingtext(text_data):
    replaced = re.sub("</?p[^>]*>", "", text_data)
    replaced = re.sub("</?div[^>]*>", "", text_data)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    return replaced

def pre_processing_html(html_data):
    final_data1 =" "
    title_value = html_data.find('h1', class_='title topictitle1 bx--type-productive-heading-06')
    body_data =  html_data.find('div', class_='body conbody')
    if title_value == None:
        final_data1 = pre_processingtext(str(html_data))
    else:
        final_data1= str(title_value)+ "  " +str(body_data)
        final_data1 = pre_processingtext(final_data1)
    return final_data1

def create_file(topic_labal,data):
    folder_name = '/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/ibm_doc_new/'
    topic_labal = topic_labal.replace("/","")
    file_name = folder_name+topic_labal+".txt"
    file1 = open(file_name,"w")
    file1.write(data)
    file1.close()


def create_html_file(topic_labal,data):
    folder_name = '/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/ibm_doc_new/HTML/'
    topic_labal = topic_labal.replace("/","")
    file_name = folder_name+topic_labal+".html"
    file1 = open(file_name,"w")
    file1.write(str(data))
    file1.close()



def inner_page_topic(topic):
    final_data=""
    if 'href' in topic:
        topic_labal = topic['label']
        href_val = topic['href']
        url ='https://www.ibm.com/docs/api/v1/content/'+str(href_val)+'?parsebody=true&lang=en'
        print(url)
        topic_page = requests.get(url)
        soup_value = BeautifulSoup(topic_page.text, 'html.parser')
        create_html_file(topic_labal,soup_value)
        sleep(np.random.randint(1, 15))
        final_data = pre_processing_html(soup_value)
    return str(final_data)


def new_version_page(url_key):
    product_data =""
    inner_page = 'https://www.ibm.com/docs/api/v1/toc/'+str(url_key)+'?lang=en'
    print("url ----",inner_page)
    inner_page_result = requests.get(inner_page)
    inner_page_json = inner_page_result.json()
    print("lenttgh  1",len(inner_page_json))
   # print(inner_page_json)
    ## traverse inner json page 
    try:
        if 'toc' in inner_page_json:
            toc_inner = inner_page_json['toc']
            if 'topics' in toc_inner:
                topics = toc_inner['topics']
                print("length 2--",len(topics))
                for topic in topics:
                    topic_data =inner_page_topic(topic)
                    product_data = product_data+" "+ topic_data
                    if 'topics' in topic:
                        inner_topics = topic['topics']
                        print("length 3--",len(inner_topics))
                        for i in range(len(inner_topics)):
                            topic2 = inner_topics[i]
                            topic_data1 =inner_page_topic(topic2)
                            product_data = product_data+" "+ topic_data1
                            if 'topics' in topic2:
                                inner_topics2 = topic2['topics']
                                for j in range(len(inner_topics2)):
                                    topic3 = inner_topics2[j]
                                    topic_data2 =inner_page_topic(topic3)
                                    product_data = product_data+" "+ topic_data2
        else:
            new_url = 'https://www.ibm.com/docs/api/v1/otherversion/'+str(url_key)+'?existingTopicsOnly=false&lang=en'
            print("url new ----",new_url)
            inner_page_result = requests.get(new_url)
            inner_page_json = inner_page_result.json()
            #print(inner_page_json)
            if 'otherVersions' in inner_page_json:
                value = inner_page_json['otherVersions']
                if 'newHref' in value[0]:
                    new_href = value[0]['newHref']
                    print("helloooo",new_href)


        product_data =remove_extra_lines(product_data)
        create_file(product_name,product_data)
        print("file created succesfully")
        return True
                
    except Exception as e:
        print("Issue ---",e)            
        data = product_name+"-----"+str(e)
        product_list_not_processed.append(data)
        print("error")
        return e



#print(json_result)
product_names_dict = []
url_keys=[]
for json_key in json_result:
    product_names_dict.append({'Product Name':json_key['name'],'URL Key':json_key['productUrlKey']})
    url_keys.append(json_key['productUrlKey'])

product_df = pd.DataFrame(product_names_dict)

## travrse product list 
i=0
product_list_not_processed =[]
print("length--",len(product_df))
print("length--",len(url_keys))
print("length--",len(set(url_keys)))
product_df1 = product_df[0:10]
print(product_df1)
file_status = False
for index,row in product_df1.iterrows():
    i=i+1
    print("Processing products--", i)
    product_data =""
    url_key = row['URL Key']
    product_name = row['Product Name']
    inner_page = 'https://www.ibm.com/docs/api/v1/toc/'+str(url_key)+'?lang=en'
    print("url ----",inner_page)
    inner_page_result = requests.get(inner_page)
    inner_page_json = inner_page_result.json()
    print("lenttgh  1",len(inner_page_json))
   # print(inner_page_json)
    ## traverse inner json page 
    try:
        if 'toc' in inner_page_json:
            toc_inner = inner_page_json['toc']
            if 'topics' in toc_inner:
                topics = toc_inner['topics']
                print("length 2--",len(topics))
                for topic in topics:
                    topic_data =inner_page_topic(topic)
                    product_data = product_data+" "+ topic_data
                    if 'topics' in topic:
                        inner_topics = topic['topics']
                        print("length 3--",len(inner_topics))
                        for i in range(len(inner_topics)):
                            topic2 = inner_topics[i]
                            topic_data1 =inner_page_topic(topic2)
                            product_data = product_data+" "+ topic_data1
                            if 'topics' in topic2:
                                inner_topics2 = topic2['topics']
                                for j in range(len(inner_topics2)):
                                    topic3 = inner_topics2[j]
                                    topic_data2 =inner_page_topic(topic3)
                                    product_data = product_data+" "+ topic_data2
        else:
            new_url = 'https://www.ibm.com/docs/api/v1/otherversion/'+str(url_key)+'?existingTopicsOnly=false&lang=en'
            print("url new ----",new_url)
            inner_page_result = requests.get(new_url)
            inner_page_json = inner_page_result.json()
            #print(inner_page_json)
            if 'otherVersions' in inner_page_json:
                value = inner_page_json['otherVersions']
                if 'newHref' in value[0]:
                    new_href = value[0]['newHref']
                    print("helloooo",new_href)
                    file_status = new_version_page(new_href)
                else:
                    new_href = value[0]['href']
                    print("helloooo",new_href)
                    file_status =new_version_page(new_href)


        if not file_status:
            product_data =remove_extra_lines(product_data)
            create_file(product_name,product_data)
            print("file created succesfully")
        
       
                
    except Exception as e:
        print("Issue ---",e)            
        data = product_name+"-----"+str(e)
        product_list_not_processed.append(data)
        print("error")
        continue
    


print("Not processed product which not mtach--", len(product_list_not_processed))
listToStr = ' , '.join([str(elem) for elem in product_list_not_processed])
create_file("not process prdouct1",listToStr)

