import requests
from bs4 import BeautifulSoup as BS
from ebooklib import epub

book = epub.EpubBook()
chapter_list=list()
#set metadata
book.set_identifier('sampleidentifier31415')
book.set_title('Worm')
book.set_language('en')
book.add_author('Wildbow')

def add_chapter(link):
    global book, chapter_list
    chapter_webpage=requests.get(link)
    soup=BS(chapter_webpage.content, 'html5lib')
    head=soup.find('h1', attrs = {'class':"entry-title"}).get_text() #title
    content=soup.find('div', attrs = {'class':"entry-content"}) #needs lfiltering
    chapter_text=str()
    for para in content('p'): #loop to make the chapter. I should find a better way
        if len(para('a'))==0:
            chapter_text+=(para.get_text()+'\n')
        else:
            pass
    chapter=epub.EpubHtml(title=head, file_name=link, lang='en') #chapter object
    chapter.set_content(chapter_text)
    book.add_item(chapter)
    chapter_list.append(chapter)
    print("Added chapter:", head)

contents_webpage=requests.get("https://parahumans.wordpress.com/table-of-contents/")
#creates a response object which you can later use with class methods
soup=BS(contents_webpage.content, 'html5lib') #soup object
content=soup.find('div', attrs = {'class':"entry-content"}) #main content
for link in content('a'): #iterate links
    try:
        link=link['href']
        assert "share" not in link #skips social media links
        #conditional statement to handle error if http not in link
        if 'https://' not in link or link.index("https://")!=0:
            link="https://"+link
        add_chapter(link)
    except (KeyError, AssertionError):
        break

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
#table of contents?
book.spine=['nav']+chapter_list
epub.write_epub('Worm.epub',book)