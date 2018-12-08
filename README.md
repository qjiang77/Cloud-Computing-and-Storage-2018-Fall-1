# Smart News Search Engine: iSearch+

This repo is the course project of Cloud Computing and Storage in 2018 Fall, University of Florida.

Authors: Yifan Wang, Jingyang Guo, Qi Jiang

Deliverable URL: https://github.com/wyfunique/Cloud-Computing-and-Storage-2018-Fall

#Introduction
iSearch+ is a distributed smart news search system that integrates data miner into search engine. 
It is aiming to search information from news articles from major news websites 
and conduct data mining analysis to extract hidden information in the news articles.


#Usage

## Configuration ##
The search system has several dependencies. They can be configured as shown in the following example:
```
$ pip install tornado
$ pip install torndb
$ pip install TextBlob
$ pip install pandas
$ pip install nltk
$ pip install numpy
```
_MySQL_, _Spark_ and _mysql-connector-java_ need to be installed using installation packages from official websites.
```
 MySQL == 5.8
 Spark == 2.3.1
 mysql-connector-java == 8.0.12
```

## Crawler ##
Before starting search, system needs to crawl recent news articles from news website.
```python
> cd news_spider/
> python3 main.py -t 3 -n 10 
> python data_cleaner.py
> python process_filename.py
> python save_article_in_db.py
> python ../generate_inverted_index.py
```

## Web Server ##
```python
> python web_server.py
# This will run the server on default port 8888
```
