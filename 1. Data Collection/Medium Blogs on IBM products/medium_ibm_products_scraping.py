from bs4 import BeautifulSoup
import requests
import math
import pandas as pd
import numpy as np
from time import sleep


# Put several of this line in different places around the code


## extract data month ,year with each day
def get_date_list(month,year):
    day_list =[]
    n_days = 30
    if month in range(1, 13):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            n_days = 31
        elif month in [4, 6, 9, 11]:
            n_days = 30
        else:
            n_days = 28

    for day in range(1, n_days + 1):
        month, day = str(month), str(day)
        if len(month) == 1:
            month = f'0{month}'
        if len(day) == 1:
            day = f'0{day}'
        day_list.append(f'{year}/{month}/{day}')
    return day_list

## pass moth n year to get all data for that month
day_list = get_date_list(2,2023)
url_list =[]
for day in day_list:
    url_list.append(f'https://medium.com/ibm-data-ai/archive/'+day)
print("day_list_size--",len(day_list))
print("url_list_size--",len(url_list))

## IBM data Ai publication
##url = 'https://medium.com/ibm-data-ai/archive/2016/09'
publication_list3 =['build-and-deploy-quantum-based-web-applications','ibm-ks','ibm-security-access-manager-recipes','ifmr-data-science-big-data-analytics-training','icp-for-data','systems-ai']

publication_list2=['qiskit-openshift-multi-arch','automate-aws-eks-resource-check','ibm-cloud-pak-for-automation','ibm-cloud-pak-tips-and-good-practices','ibm-journal']

publication_list = ['databand-ai','art-of-quantum','ibmresearch','ibm-watson-aiops','ibm-dcpe-group','ibm-business-automation-ap-el','smarter-workforce-design','ibm-journey-designer','multi-cloud-management']
publication_list1 = ['ibm-cloud-paks-help-and-guidance-from-ibm-cloud','ibm-watson-speech-services']
publication_list4=['ics-ibm-connections','ibm-docs','seattle-car-accident-severity-ibm-capstone-project','openshift-in-ibmcloud','ibm-cloud-infrastructure-as-code','openshift-on-z','cognitivewithout']

year_list =['2016','2017','2018','2019','2020','2021','2022','2023']
url_list =[]
for pub in publication_list:
    for year in year_list:
        for  month in range(1, 13):
            url_list.append('https://medium.com/'+str(pub)+'/archive/'+str(year)+'/'+str(month))

#url = 'https://medium.com/ibm-watson/archive/2023/04'


for url in url_list:
    stories_data = []
    # here need to be pass publication name url form where we want to extract the data
    sleep(np.random.randint(1, 15))
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    stories = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')
    print("length---",len(stories))
    print("URL",url, "length---",len(stories))
    for story in stories:
        medium_data =''
        each_story = []
        author_box = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
        author_url = author_box.find('a')['href']
        try:
            reading_time = author_box.find('span', class_='readingTime')['title']
        except:
            continue

        title = story.find('h3').text if story.find('h3') else '-'
        subtitle = story.find('h4').text if story.find('h4') else '-'
        print("title---",title)
        medium_data= medium_data+ " "+title+" "+ subtitle
            

        if story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents'):
            claps = story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents').text
        else:
            claps = 0

        if story.find('a', class_='button button--chromeless u-baseColor--buttonNormal'): 
            responses = story.find('a', class_='button button--chromeless u-baseColor--buttonNormal').text
        else:
            responses = '0 responses'
        try:
            story_url = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')['href']
        except:
            continue

        story_page = requests.get(story_url)
        story_soup = BeautifulSoup(story_page.text, 'html.parser')

        sections = story_soup.find_all('section')
        story_paragraphs = []
        section_titles = [] 

        for section in sections:
            paragraphs = section.find_all('p')
            for paragraph in paragraphs:
                story_paragraphs.append(paragraph.text)
                medium_data= medium_data+ " "+paragraph.text+" \n"
            subs = section.find_all('h1')
            for sub in subs:
                section_titles.append(sub.text)

            number_sections = len(section_titles)
            number_paragraphs = len(story_paragraphs)


            each_story.append(title)
            each_story.append(subtitle)
            each_story.append(claps)
            each_story.append(responses)
            each_story.append(author_url)
            each_story.append(story_url)
            each_story.append(reading_time)
            each_story.append(number_sections)
            each_story.append(section_titles)
            each_story.append(number_paragraphs)
            each_story.append(story_paragraphs)
            stories_data.append(each_story)

            columns = [ 'title', 'subtitle', 'claps', 'responses', 
                'author_url', 'story_url', 'reading_time (mins)', 
                'number_sections', 'section_titles', 
                'number_paragraphs','story_paragraphs']

            title = title.replace("/","")
            df = pd.DataFrame(stories_data, columns=columns)
            file_name = "/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/Medium/csv/"+title+".csv"
            text_file_name = "/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/Medium/text/"+title+".txt"
            df.to_csv(file_name, sep='\t', index=False)

            file1 = open(text_file_name,"w")
            file1.write(medium_data)
            file1.close()



