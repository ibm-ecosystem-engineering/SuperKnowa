from bs4 import BeautifulSoup
import requests
import math
import os
import urllib.parse as encoder
import random
from datetime import date
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
base_link = 'https://www.itexams.com/vendor/IBM'

result = requests.get(base_link, headers=headers)
soup = BeautifulSoup(result.content, "html.parser")
#soup.prettify()

exam_base_url = 'https://www.itexams.com/exam'

def scrap_question(soup):
    question_list = []
    for div in soup.find_all('div', class_="question_block"):
        #print(div.prettify())
        question = {}

        for ques in div.find_all('div', class_='question_text'):
            question["question"] = ques.text.strip()
            #print(question)
        
        choice_list = []
        for choiceoptions in div.find_all('ul', class_='choices-list'):
            for choice in choiceoptions.find_all('li'):
                choice_list.append(choice.text.strip())
        question["options"] = choice_list

        for ans in div.find_all('div', class_='answer_block'):
            question["answer"] = ans.text.replace(' ','').replace('\n', '').strip()
    
        question_list.append(question)
    return question_list

numberOfQuestion = 0
for a in soup.find_all('a', href=re.compile("^/info")):
    examCode = os.path.basename(a['href'])
    title = a.text.strip()
    title = re.sub(r'[\\/*?:"<>|]',"",title)

    exam_url = f"{exam_base_url}/{examCode}"

    print(f"exam code: {examCode}, exam: {title}")

    exam_content = requests.get(exam_url, headers=headers)

    soup = BeautifulSoup(exam_content.content, "html.parser")
    question_list = scrap_question(soup)
    json_object = json.dumps(question_list, indent=4)
    numberOfQuestion = numberOfQuestion + len(question_list)
   # Writing to sample.json
    with open(f"exam/{title}.json", "w") as outfile:
        outfile.write(json_object)

print(f"Total number of question #{numberOfQuestion}")