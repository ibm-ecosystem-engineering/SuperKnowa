import pysolr
import os
import tika
tika.initVM()
from tika import parser  
import re
from datetime import date
import pandas as pd
import json
from datetime import datetime
import requests
import PyPDF2

from pathlib import Path
from dateutil.parser import parse

## get today's date
today = date.today()
print("Today's date:", today)

## get all files from folder
def get_all_files(folder_name):
    # Change the directory
    os.chdir(folder_name)
    # iterate through all file
    file_path_list =[]
    for file in os.listdir():
        if ".txt" in file:
            file_path = f"{folder_name}/{file}"
            file_path_list.append(file_path)
    return file_path_list

def readdata_frompdf(file_name):
    content=''
    try:
        pdfFileObj = open(file_name, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            pageObj = pdfReader.pages[i]
            content =content+" "+pageObj.extract_text()

        pdfFileObj.close()
        return content
    except:
         print("file is empty")
         return content

def pre_processingtext(text_data):
    replaced = re.sub("</?p[^>]*>", "", text_data)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("id=*>;", "", replaced)
    return replaced

def index_ibm_developerdata():
    with open(file_path, 'r', encoding="latin1") as file:
        if ".txt" in file_path:
            content = file.read()
            print(len(content), file_path)
            content_value = content.split("content:")
            content = pre_processingtext(content_value[1])
            categories_val = content_value[0].split("categories:")
            categories = categories_val[1]
            sub_title =  categories_val[0].split("sub_title:")
            title_val =  sub_title[0].split("title:")
            title = title_val[1]
            pd_val =  title_val[0].split("publish_date:")
            publish_date = pd_val[1]
            ld_val =  pd_val[0].split("updated_date:")
            updated_date = ld_val[1]
            print("values ---",len(ld_val))
            urls =  ld_val[0].split("URL:")
            print(len(urls))
            #https://developer.ibm.com/blogs/
           # url = "https://developer.ibm.com/middleware/v1/contents"+urls[1]
            url = "https://developer.ibm.com/blogs/"+urls[1]

            indexing_date = today
            source = "IBM Developer"
            data = "{'id' : '"+str(title)+"', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'}"
            #df = pd.DataFrame({'id' : '""+str(title)+""', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'},index=[i])
            #print(df.to_json(orient="split"))
            
            #json_object = json.loads(data)
            publish_date = publish_date.replace("\n","").strip()
            updated_date = updated_date.replace("\n","").strip()
            print(publish_date)
            print("update_date ",updated_date)
            publish_date_obj = datetime.strptime(publish_date,"%Y-%m-%dT%H:%M:%S")
            publish_date = publish_date_obj.date()

            updated_date_obj = datetime.strptime(updated_date,"%Y-%m-%dT%H:%M:%S")
            updated_date = updated_date_obj.date()

        
            solrdocs.append({
            "id": ""+title+"",
            "published_source": ""+source+"",
            "publish_date": ""+str(publish_date)+"",
            "last_update_date": ""+str(updated_date)+"",
            "indexing_date": ""+str(indexing_date)+"",
            "content": ""+content+"",
            "url": ""+url+"",
            "keywords": ""+str(sub_title)+"",
            "categories": ""+str(categories)+"",
        })
        
def indexwhitepaerdata():
    for filename in os.listdir(white_paper_docs_dir):
        print("processing i---",i)
        file_path = os.path.join(white_paper_docs_dir, filename)
        
        # Read the contents of the file
        headers = {
                "X-Tika-OCRLanguage": "eng",
                "X-Tika-OCRTimeout": "300"
            }
        with open(file_path, 'r', encoding="latin1") as file:
            extracted_text=''
            if ".json" in file_path:
                content = file.read()
                json_object = json.loads(content)
                #print(json_object)
                source ="IBM White Paper"
                publish_date = json_object['publish_date']
                if publish_date is not None:
                    dt = parse(publish_date)
                    publish_date=dt.strftime('%Y-%d-%m')
                else:
                    publish_date = today
                updated_date = publish_date
                indexing_date = today
                url = json_object['url']
                attachment = json_object['attachment']
                title = json_object['title']
                j=1
                if len(attachment) >1:
                    for att in attachment:
                        print("Value",att)     
                        #file_name = att.replace("https://www.ibm.com/support/pages/system/files/inline-files/","")
                        file_name = os.path.basename(att)
                        print(file_name)
                        file_path = white_paper_docs_dir+file_name
                        path = Path(file_path)
                        if path.is_file():
                            #parsed_content = parser.from_file(file_path,requestOptions={'headers': headers, 'timeout': 500})
                            # Get the extracted text
                            #extracted_text = parsed_content['content']
                            extracted_text =readdata_frompdf(file_path)
                        else:
                            print("file_name",file_name)
                            try:
                                downloadFile(att,white_paper_docs_dir+"/"+file_name)
                                if path.is_file():
                                    #parsed_content = parser.from_file(file_path,requestOptions={'headers': headers, 'timeout': 500})
                                    # Get the extracted text
                                    #extracted_text = parsed_content['content']
                                    extracted_text =readdata_frompdf(file_path)
                            except:
                                print("file in not available")
                                break

                        title = title+"_"+str(i)
                        if extracted_text is not None:
                            solrdocs.append({
                    "id": ""+title+"",
                    "published_source": ""+source+"",
                    "publish_date": ""+str(publish_date)+"",
                    "last_update_date": ""+str(updated_date)+"",
                    "indexing_date": ""+str(indexing_date)+"",
                    "content": ""+extracted_text+"",
                    "url": ""+url+"",
                    "keywords": "",
                    "categories": "",
                })
                            
                else:
                    if len(attachment) ==1:
                        file_name = os.path.basename(attachment[0])
                        print(file_name)
                        file_path = white_paper_docs_dir+file_name
                        path = Path(file_path)
                        if path.is_file():
                            #parsed_content = parser.from_file(file_path,requestOptions={'headers': headers, 'timeout': 500})
                            #extracted_text = parsed_content['content']
                            extracted_text = readdata_frompdf(file_path)
                        if extracted_text is not None:
                            solrdocs.append({
                        "id": ""+title+"",
                        "published_source": ""+source+"",
                        "publish_date": ""+str(publish_date)+"",
                        "last_update_date": ""+str(updated_date)+"",
                        "indexing_date": ""+str(indexing_date)+"",
                        "content": ""+extracted_text+"",
                        "url": ""+url+"",
                        "keywords": "",
                        "categories": "",
                })

    
def redbooks_indexing():
    for filename in os.listdir(redbooks_data_dir):
        print("processing i---",i)
        file_path = os.path.join(redbooks_data_dir, filename)
        
        with open(file_path, 'r', encoding="latin1") as file:
            extracted_text=''
            if ".json" in file_path:
                content = file.read()
                source ="Redbooks"
                content_list = content.split("\n")
                publish_date = content_list[2].replace("publish_date: ","")
                updated_date = content_list[1].replace("updated_date: ","")
                if updated_date is None:
                    updated_date = publish_date
                indexing_date = today
                url = content_list[0].replace("URL: ","")
                file_name = content_list[3].replace("file_name: ","")
                print(file_name)
                file_path= redbooks_data_dir+file_name
                extracted_text = readdata_frompdf(file_path)
                if extracted_text is not None:
                                solrdocs.append({
                            "id": ""+file_name.replace(".pdf","")+"",
                            "published_source": ""+source+"",
                            "publish_date": ""+str(publish_date)+"",
                            "last_update_date": ""+str(updated_date)+"",
                            "indexing_date": ""+str(indexing_date)+"",
                            "content": ""+extracted_text+"",
                            "url": ""+url+"",
                            "keywords": "",
                            "categories": "",
                    })

                if i ==100:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 200:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 300:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 400:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 500:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 600:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 700:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 800:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 900:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 1000:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 1100:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                if i == 1200:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                i=i+1

def ibm_cloud_docs():
    with open(ibm_cloud_metadta_file, 'r', encoding="latin1") as file:
        content = file.read()
        content_list = content.split("\n")
        print(len(content_list))
        for content in content_list:
            try:
                print("process---",i)
                print("solr index process---",j)
                file_names = content.split("file name")
                url_data = file_names[1].split("Url")
                file_name = url_data[0].replace("\": ","").replace(",\"","").replace("\"","")
                metadata = url_data[1].split("metadata")
                url = metadata[0].replace("\": ","").replace(", \"","")
                lastupdated = metadata[1].split("lastupdated:")
                if len(lastupdated) >1:
                    last_updated_data = lastupdated[1].split("keywords:")
                    if len(last_updated_data) >1:
                        keywords = last_updated_data[1].replace("\"}","")
                    else:
                        keywords=""
                else:
                    keywords=""
                last_updated = last_updated_data[0].replace("\"","").strip().replace(" subcollection: assistant }","").split(" ")[0]
                if len(last_updated) < 6:
                    last_updated = today
                else:
                    if '/' in last_updated:
                        last_updated = last_updated.replace("/","-") 
                last_updated=last_updated.encode("ascii", "ignore")
                last_updated = last_updated.replace("b'","-") 
            
                
                with open(file_name, 'r', encoding="latin1") as file:
                    extracted_text=''
                    extracted_text = file.read()
                    source ="IBM Developer docs"
                    print(content)
                
                file_name_val = file_name.replace("/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_process_metdata_new/","")
                id = file_name_val.replace(".txt","")+"_"+source+str(i)
                if extracted_text is not None:
                            solrdocs.append({
                                    "id": ""+file_name_val.replace(".txt","")+"",
                                    "published_source": ""+source+"",
                                    "publish_date": ""+str(last_updated)+"",
                                    "last_update_date": ""+str(last_updated)+"",
                                    "indexing_date": ""+str(today)+"",
                                    "content": ""+extracted_text+"",
                                    "url": ""+url+"",
                                    "keywords": ""+keywords+"",
                                    "categories": "",
                            })
            except:
                i = i+1
                continue
            
            if j == 100:
                try:
                    solr.add(solrdocs)
                    print("indexed data scussefully")
                    solrdocs=[]
                    j = -1
                except:
                    j = -1
                    continue

def ibm_doc_index():
    for filename in os.listdir(ibm_docs_dir):
        file_path = os.path.join(ibm_docs_dir, filename)
        with open(file_path, 'r', encoding="latin1") as file:
                if ".txt" in file_path:
                    content = file.read()
                    print(len(content), file_path)
                    content_value = content.split("content:")
                    content = pre_processingtext(content_value[1])
                    categories_val = content_value[0].split("categories:")
                    categories = categories_val[1]
                    sub_title =  categories_val[0].split("sub_title:")
                    title_val =  sub_title[0].split("title:")
                    title = title_val[1]
                    pd_val =  title_val[0].split("publish_date:")
                    publish_date = pd_val[1]
                    ld_val =  pd_val[0].split("updated_date:")
                    updated_date = ld_val[1]
                    print("values ---",len(ld_val))
                    urls =  ld_val[0].split("URL:")
                    print(len(urls))
                    #https://developer.ibm.com/blogs/
                # url = "https://developer.ibm.com/middleware/v1/contents"+urls[1]
                    url = "https://developer.ibm.com"+urls[1].strip()+'/'

                    indexing_date = today
                    source = "IBM Developer"
                    data = "{'id' : '"+str(title)+"', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'}"
                    #df = pd.DataFrame({'id' : '""+str(title)+""', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'},index=[i])
                    #print(df.to_json(orient="split"))
                    
                    #json_object = json.loads(data)
                    publish_date = publish_date.replace("\n","").strip()
                    updated_date = updated_date.replace("\n","").strip()
                    print(publish_date)
                    print("update_date ",updated_date)
                    publish_date_obj = datetime.strptime(publish_date,"%Y-%m-%dT%H:%M:%S")
                    publish_date = publish_date_obj.date()

                    updated_date_obj = datetime.strptime(updated_date,"%Y-%m-%dT%H:%M:%S")
                    updated_date = updated_date_obj.date()

                
                    solrdocs.append({
                    "id": ""+title+"",
                    "published_source": ""+source+"",
                    "publish_date": ""+str(publish_date)+"",
                    "last_update_date": ""+str(updated_date)+"",
                    "indexing_date": ""+str(indexing_date)+"",
                    "content": ""+content+"",
                    "url": ""+url+"",
                    "keywords": ""+str(sub_title)+"",
                    "categories": ""+str(categories)+"",
                })



        

def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

# Connect to Solr
solr = pysolr.Solr('http://150.239.171.68:8983/solr/superknowa/', always_commit=True,timeout=50)

# Directory containing the documents
ibm_docs_dir = '/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/ibm_developer_metadata/'
white_paper_docs_dir ='/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/white_paper_metadata/data-2/'
redbooks_data_dir ='/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/redbooks_data/'
ibm_cloud_docs_dir ='/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_process_metdata_new/'
ibm_cloud_metadta_file ='/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_metadata5.txt'
ibm_medium_blog ='/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/Medium/text'
ibm_medium_blog_csv ='/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/Medium/csv'


# Iterate over the files in the directory
solrdocs =[]
i = 0
j = 0
file_path_list_medium = get_all_files(ibm_medium_blog)
print(type(file_path_list_medium))
for filename in os.listdir(ibm_medium_blog_csv):
    file_path = os.path.join(ibm_medium_blog_csv, filename)
    with open(file_path, 'r', encoding="latin1") as file:
            if ".csv" in file_path:
                content = ''
                df = pd.read_csv(file_path, sep='\t')
                for ind in df.index:
                    title = df['title'][ind]
                    sub_title = df['subtitle'][ind]
                    url  =  df['story_url'][ind]
                    publish_date = today
                    updated_date = today
                    file_name = str(ibm_medium_blog+"/"+title+".txt")
                    print(file_name)
                    if file_name in file_path_list_medium:
                        with open(file_name, 'r', encoding="latin1") as file1:
                                content = file1.read()
                               
                    indexing_date = today
                    source = "Medium"
                    categories=''
                    
                    print(content)

                    solrdocs.append({
                        "id": ""+title+"",
                        "published_source": ""+source+"",
                        "publish_date": ""+str(publish_date)+"",
                        "last_update_date": ""+str(updated_date)+"",
                        "indexing_date": ""+str(indexing_date)+"",
                        "content": ""+content+"",
                        "url": ""+url+"",
                        "keywords": ""+str(sub_title)+"",
                        "categories": ""+str(categories)+"",
                    })

solr.add(solrdocs)
print("indexed data scussefully")



#print(solrdocs)
#df = pd.DataFrame(solrdocs)
#data_json = df.to_json()
#solrdocs_new =[]
#solrdocs_new.append(data_json)
#print(df.to_json())

#solr.add(solrdocs)
#print("indexed data scussefully")



