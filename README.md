# Ebook-Scraper
This program iterates through the links in the [Table of Contents](https://parahumans.wordpress.com/table-of-contents/) to make an ebook for Worm

**The following has to be kept in mind:**
* The program uses the modules `beautifulsoup4`, `requests` and `lxml` to parse through the contents of the webpage. The modules can be installed with pip before running the program. The program also uses the`zipfile` module to create the .epub file.
* The program does not use style sheets and page templates for the epub

The structure of the epub file is as follows
- OEBPS
  - Text (This contains all the chapters)
  - Images (This contains images used in the book. In this case, it just stores the cover image)
  - content.opf
  - start.xhtml
  - toc.ncx (The table of contents)
- META-INF
  - container.xml
- mimetype
