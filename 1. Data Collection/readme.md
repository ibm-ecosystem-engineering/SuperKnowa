# Data Scraping

This folder contains code for scraping and cleaning data from various sources as listed below:

- [IBM Cloud Documentation](../1.%20Data%20Collection/IBM%20Cloud%20Documentation/): All the markdown files are first downloaded from GitHub
    - [Doc_Cleaning.py](../1.%20Data%20Collection/IBM%20Cloud%20Documentation/Doc_Cleaning%20.py): Cleans markdown files
    - [md_convert_html.py](../1.%20Data%20Collection/IBM%20Cloud%20Documentation/md_convert_html.py): Convert markdown files into HTML
- [IBM Developer](../1.%20Data%20Collection/IBM%20Developer/): Scraping data from IBM developer
    - [ibm_developer_scraping.py](../1.%20Data%20Collection/IBM%20Developer/ibm_developer_scraping.py): scrapes blogs, articles, tutorials and code patterns from IBM developer
- [IBM Product Documentation](../1.%20Data%20Collection/IBM%20Product%20Documentations/): Scraping data from IBM products website and GitHub Markdowns
    - [ibm_product_doc_md.py](../1.%20Data%20Collection/IBM%20Product%20Documentations/ibm_product_doc_md.py): Cleans markdown files for IBM product docs
    - [ibm_product_doc_scraping.py](../1.%20Data%20Collection/IBM%20Product%20Documentations/ibm_product_doc_scraping.py): Scrapes IBM's product documentation recursively
- [IBM Redbooks](../1.%20Data%20Collection/IBM%20Redbooks/): Scraping data from IBM Redbooks
    - [redbooks_scrapper.py](../1.%20Data%20Collection/IBM%20Redbooks/redbooks_scrapper.py): Scrapes all the IBM redbooks recursively
- [IBM Test](../1.%20Data%20Collection/IBM%20Test%20/): Scraping Questions and Answers from IBM's IT exams
    - [it_exam_scraping]: Scrapes all the IBM's IT exams available for free
- [IBM Whitepapers](../1.%20Data%20Collection/IBM%20Whitepapers/): Scraping data from IBM Whitepapers
    - [ibm_whitepaper.py](../1.%20Data%20Collection/IBM%20Whitepapers/ibm_white_paper.py): Scrapes all the IBM White papers recursively
- [Medium Blogs on IBM products](../1.%20Data%20Collection/Medium%20Blogs%20on%20IBM%20products/): Scraping data from Medium related to IBM products
    - [medium_ibm_products_scraping.py](../1.%20Data%20Collection/Medium%20Blogs%20on%20IBM%20products/medium_ibm_products_scraping.py): Scrapes all the Medium blogs related to IBM products
- [Total Page Count](../1.%20Data%20Collection/Total%20Page%20Count/): Counting total number of pages in the corpus
    - [token_page_count.ipynb](../1.%20Data%20Collection/Total%20Page%20Count/token_page_count.ipynb): Notebook for analyzing and counting total number of tokens and pages in the corpus/collection

## Steps for running a scraper:

### Create a virutal environment

```sh
python3 -m venv scrape
```

### Activate environment

```sh
source scrape/bin/activate
```

### Install required library

```sh
pip3 install -r requirements.txt 
```

## Start the program (ex: IBM Developer scraping)

```sh
python3 ibm_developer_scraping.py
```
