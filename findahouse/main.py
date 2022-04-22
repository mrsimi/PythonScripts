from distutils import bcppcompiler
from unittest import result
from bs4 import BeautifulSoup as BS
import json
import requests


class ContentDto:
    def __init__(self, title, link):
        self.title = title, 
        self.link = link
    

def contains_query(data, query1, query2, query3):
    sentence = data.split(" ")

    for word in sentence:
        if query1 == word or (len(query2)> 0 and query2 in word) or (len(query3) > 0 and query3 in word):
            return True
        
    return False

def create_json(datalist):
    with open("results.json", "w") as file:
        json.dump([ob.__dict__ for ob in datalist], file, indent=4, sort_keys=True)

def run(query1, query2='', query3=''):
    search_results = []
    base_url = 'https://www.nairaland.com/'
    ref_url = 'properties'
    url_format = base_url + ref_url+'/page'

    for i in range(0, 20):
        
        url = url_format.replace('page', str(i))
        print('crawling page ----' + url)
        page = requests.get(url)
        soup = BS(page.content, 'html.parser')

        td_list = soup.find_all('td')

        for td in td_list: 
            b_content = td.find('b')
            content_topic = b_content.text.lower()

            if contains_query(content_topic, query1, query2, query3):
                a_content = td.find_all('a')
                content_link = a_content[1].get('href')
                content_link = base_url+content_link

                search_results.append(ContentDto(content_topic, content_link))

    print('done')
    #create_json(search_results)
    

    print(json.dumps([ob.__dict__ for ob in search_results], indent=2, sort_keys=True))

if __name__ == "__main__":
    run('rent')


