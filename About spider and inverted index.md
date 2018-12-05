### Important files for the spider
**1. main.py**
  The main program file of the news spider.
  ```
  python3 main.py -t 5 -n 10
  ```
  Parameter `t` indicates the number of threads to crawl each news source.
  Parameter `n` indicates the number of news sources we will crawl.
  
**2. data_cleaner.py**
  The file for removing empty news folders from crawled results.
  
**3. process_filename.py**
  The file for processing filenames of crawled news articles, like removing non-ascii characters, to avoid error when saving articles into database.

**4. save_article_in_db.py**
  The file for saving crawled articles into database.

**NOTE:**
(1) You must run these files in specific order: main.py -> data_cleaner.py -> process_filename.py -> save_article_in_db.py
(2) Before running save_article_in_db.py, make sure there is a table named "article" in your database.

### Generate inverted index
First, make sure there is a table named "inverted_index" in your database.
Second, run the file "generate_inverted_index.py". 
