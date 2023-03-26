import requests
from bs4 import BeautifulSoup as BS
import zipfile

def remove_special_characters(text):
    out=str()
    for char in text:
        if char.isalnum() or char in ' .()':
            out+=char
    return out

def write(content,title):
    text=content.prettify()
    text='<center><h1>%s</h1></center>' % (title) +text
    path='OEBPS/Text/'+title+'.html'
    epub.writestr(path,text)

title_list=list()

def add_chapter(link):
    chapter_webpage=requests.get(link)
    soup=BS(chapter_webpage.content,'lxml') 
    title=soup.find('h1', attrs = {'class':"entry-title"}).get_text() #title
    title=remove_special_characters(title)
    if title in title_list:
        return title
    content=soup.find('div', attrs = {'class':"entry-content"}) #needs filtering
    
    #iterate through links and remove them 
    for a in content.findAll('a',href=True):
        a.extract()
    #remove the Social media flairs
    for a in content.findAll('div', attrs ={"id":'jp-post-flair'}):
        a.extract()
    
    write(content,title)
    print("Added chapter:", title)
    return title

epub=zipfile.ZipFile('Worm.epub','w')

#mimetype
epub.writestr("mimetype","application/epub+zip")

epub.writestr("META-INF/container.xml",'''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
''')

image_url=requests.get('https://static.wikia.nocookie.net/parahumans/images/d/d3/Skitter_by_ariirf.jpg/')
epub.writestr('OEBPS/Images/cover.jpg',image_url.content)
print('Cover added')

contents_webpage=requests.get("https://parahumans.wordpress.com/table-of-contents/")
soup=BS(contents_webpage.content,'lxml') #soup object
content=soup.find('div', attrs = {'class':"entry-content"}) #main content
for link in content('a'): #iterate links
    try:
        link=link['href']
        if "share" in link:
            continue #skips social media links
        
        #conditional statement to handle error if http not in link. Could be handled better
        if 'https://' not in link or link.index("https://")!=0:
            link="https://"+link
        
        title=add_chapter(link)
        if title in title_list: #some links are accidentally repeated
            continue
        title_list.append(title)
        
        # The author left out the link for the second chapter of the epilogue from the table of contants as a joke. That has to be added separately
        if title=="Teneral e.1":
            title=add_chapter('https://parahumans.wordpress.com/2013/11/05/teneral-e-2/')
            title_list.append(title)
    except (KeyError,AssertionError):
        pass

manifest=''
spine=''
toc=''

epub.writestr('OEBPS/start.xhtml','''
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">

<head>
  <title>Worm</title>
</head>

<body>
  <h1>Worm</h1>
</body>

</html>
''')

for num,title in enumerate(title_list):
    item=title+'.html'
    toc+='''
    <navPoint id="%s" playorder="%s">
        <navLabel>
            <text>%s</text>
        </navLabel>
        <content src="Text/%s"/>
    </navPoint>
    ''' % (item,num+1,title,item)
    manifest+='<item id="%s" href="Text/%s" media-type="application/xhtml+xml"/>\n        ' % (item,item)
    spine+='<itemref idref="%s" />\n        ' % (item)

epub.writestr('OEBPS/toc.ncx','''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
<head>
    <meta name="dtb:uid" content="cd751626-b72f-11ed-afa1-0242ac120002"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle>
    <text>Worm</text>
</docTitle>
<navMap>
%s
</navMap>
</ncx>
''' % (toc)
)
print("TOC Added")

content='''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>Worm</dc:title>
    	<dc:language>en</dc:language>
        <dc:creator opf:role="aut">Wildbow</dc:creator>
        <dc:identifier id="uuid_id" opf:scheme="uuid">cd751626-b72f-11ed-afa1-0242ac120002</dc:identifier>
    </metadata>
    <manifest>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="cover.jpg" properties="cover-image" href="Images/cover.jpg" media-type="image/jpg"/>
        <item href="start.xhtml" id="start" media-type="application/xhtml+xml"/>
        %s
    </manifest>
    <spine toc="ncx">
        %s
    </spine>
    <guide/>
</package>
'''

epub.writestr('OEBPS/content.opf', content % (manifest,spine))
print("Spine and Manifest added")
