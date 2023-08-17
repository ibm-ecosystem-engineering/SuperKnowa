## Import pre-required all libs.
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
import yaml

#Reading the content of config file
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfg = cfg['parsing']

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

## Reading data from pdf file
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

##  removing html tags from HTML files.
def pre_processingtext(text_data):
    replaced = re.sub("</?p[^>]*>", "", text_data)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("id=*>;", "", replaced)
    return replaced

def remove_extra_lines(data):
    data =re.sub(r'\n\s*\n', '\n', data, flags=re.MULTILINE)
    return data


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

def create_file(file_name,data):
    file_name = file_name.replace(".html",".txt").replace(".pdf",".txt")
    file1 = open(file_name,"w")
    file1.write(data)
    file1.close()


def get_parse_data(file_path):
    content =''
    if '.pdf' in file_path:
        content = readdata_frompdf(file_path)
    else:
        with open(file_path, 'r', encoding="latin1") as file:
            content = file.read()
    
    content = pre_processingtext(content)
    content = remove_extra_lines(content)
    return content


file_list = get_all_files(cfg['parsingFileFolderPath'])
for file in file_list:
    content =get_parse_data(file)
    create_file(file, content)
    print("Cleaned content sucessfully saved")
