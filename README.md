# Ebook-Scrapper
This program iterates through the links in the [Table of Contents](https://parahumans.wordpress.com/table-of-contents/) to make an ebook for Worm

**The following has to be kept in mind:**
* The program uses the modules `beautifulsoup4` and `lxml` to parse through the contents of the webpage. The modules can be installed with pip before running the program. The program also uses the`zipfile` module to create the .epub file.
* The program does not use style sheets and page templates for the epub
* Within the epub file, all the files are grouped together, and not arranged neatly into folders
* The program is based on the Table of contents page, and therefore a couple of chapters may be missing due to improper formatting of the page
