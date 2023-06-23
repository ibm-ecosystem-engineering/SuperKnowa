from bs4 import BeautifulSoup
import requests
import math

page_size=100
first_page = 'https://www-api.ibm.com/search/api/v1-1/ibmcom/appid/dw/responseFormat/json?scope=dw&rmdt=ALL&appid=dw&sortby=&appid=dw&cachebust=1681750438528&dict=spelling&facet=%7B%22id%22%3A%22DW.ContentType%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Technology%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Component%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Solution%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Language%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Practice%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Industry%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&featureFlags=7-9&filter=%28%28DWContentType%3A%22Tutorials%22%20OR%20DWContentType%3A%22Articles%22%20OR%20DWContentType%3A%22Blog%20posts%22%29%29%20AND%20%28language%3Aen%29&fr=0&languageSelector=undefined-undefined&nr=20&page=1&ql=en&query=%20&rc=us&refinement=&rmdt=entitled%2Ceassemimagenumbers%2Citstrainingtype&scope=dw&sm=true&smnr=20&variant=pvboost%3A1'

result = requests.get(first_page)

json_result = result.json()

tatal_number_of_link = json_result['resultset']['searchresults']['totalresults']

total_page = math.ceil(tatal_number_of_link/page_size)

print("Page Size: ", page_size, ", Total article/blog: ", tatal_number_of_link, ", Total number of page: ", total_page)

page_from = 0
all_articles = []

## Collect all the articles and blog links from ibm api's
with open("data/all_url.txt", "+a") as file:
    for page_number in range(1, total_page + 1):
        mainPage = f'https://www-api.ibm.com/search/api/v1-1/ibmcom/appid/dw/responseFormat/json?scope=dw&rmdt=ALL&appid=dw&sortby=&appid=dw&cachebust=1681750438528&dict=spelling&facet=%7B%22id%22%3A%22DW.ContentType%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Technology%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Component%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Solution%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Language%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Practice%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&facet=%7B%22id%22%3A%22DW.Industry%22%2C%22hierarchy%22%3A%22no%22%2C%22sortBy%22%3A%22weight%22%2C%20%22sortOrder%22%3A%22DESC%22%2C%22count%22%3A%22ALL%22%7D&featureFlags=7-9&filter=%28%28DWContentType%3A%22Tutorials%22%20OR%20DWContentType%3A%22Articles%22%20OR%20DWContentType%3A%22Blog%20posts%22%29%29%20AND%20%28language%3Aen%29&fr={page_from}&languageSelector=undefined-undefined&nr={page_size}&page={page_number}&ql=en&query=%20&rc=us&refinement=&rmdt=entitled%2Ceassemimagenumbers%2Citstrainingtype&scope=dw&sm=true&smnr=20&variant=pvboost%3A1'

        page_from = page_from + page_size

        result = requests.get(mainPage).json()

        link_list = result['resultset']['searchresults']['searchresultlist']
        
        for input_url in link_list:
            # trim ibm developer link
            parsed_link = input_url['url']
            file.write(parsed_link + '\n')

            # nlink = link[25:len(link)]
            nlink = parsed_link[25:len(parsed_link)]
            all_articles.append(nlink)

print(f'Total number of article read: {len(all_articles)}')

## fetch the articles and blog from the links
base_url = 'https://developer.ibm.com/middleware/v1/contents'
#            https://developer.ibm.com/middleware/v1/contents/tutorials/using-sap-odata-with-datastage-on-cloud-pak-for-data
#            https://developer.ibm.com/middleware/v1/contents/tutorials/using-sap-odata-with-datastage-on-cloud-pak-for-data

for i in range(len(all_articles)):
    try:
        url = base_url + all_articles[i]
        print('requesting url = ', url)
        result = requests.get(url).json()

   

        for rs in result['results']:
            soup = BeautifulSoup(rs['content'], "html.parser")

#            text = " "
#            all_p = soup.find_all("p")
#            for p in all_p:
#                text = p.text + text
            
            with open("data/"+str(i) + ".txt", "+w") as fp:
                fp.write(soup.text)
        
#        with open(str(i) + "-url.txt", "+w") as ur:
#                ur.write(url) 
    except:
        print("Faild: " + url)