import requests
import os
from bs4 import BeautifulSoup as BS

#generates path for object and makes directories if absent
def file_path(title,arc):
    path=os.path.join('./Worm_Chapters',arc)
    name='_'.join(title.split())+'.html'
    if not os.path.exists(path):
        os.mkdir(path)
    return os.path.join(path,name)

def add_chapter(link,arc):
    chapter_webpage=requests.get(link)
    soup=BS(chapter_webpage.content) 
    title=soup.find('h1', attrs = {'class':"entry-title"}).get_text() #title
    content=soup.find('div', attrs = {'class':"entry-content"}) #needs filtering
    #iterate through links and remove them 
    for a in content.findAll('a',href=True):
        a.extract()
    path=file_path(title,arc)
    file=open(path,'w')
    file.write(content.prettify())
    file.close()
    print("Added chapter:", title)

contents_webpage=requests.get("https://parahumans.wordpress.com/table-of-contents/")
#creates a response object which you can later use with class methods
soup=BS(contents_webpage.content) #soup object
content=soup.find('div', attrs = {'class':"entry-content"}) #main content
for link in content('a'): #iterate links
    if not os.path.exists('./Worm_Chapters'):
        os.mkdir('./Worm_Chapters')
    try:
        arc=link.get_text().strip()
        try:
            arc=arc[:arc.index('.')]
        except:
            continue
        link=link['href']
        assert "share" not in link #skips social media links
        #conditional statement to handle error if http not in link
        if 'https://' not in link or link.index("https://")!=0:
            link="https://"+link
        add_chapter(link,arc)
    except (KeyError, AssertionError):
        break