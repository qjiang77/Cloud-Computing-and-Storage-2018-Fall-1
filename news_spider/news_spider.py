import argparse
import codecs
import logging
import newspaper
import os
import random
import re
import redis
import setproctitle
import threading
import time
from datetime import datetime
from queue import Queue
from spider_framework import Spider

#logging.basicConfig(filename='news_spider.log', level=logging.INFO)

def getFormattedTime():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def emptyAppendOpen(filename):
	f = codecs.open(filename, 'w+', "utf-8")
	f.write('')
	f.close()
	return codecs.open(filename, 'a', "utf-8")

def printLogInfo(info, level):
	try:
		printing_str = "[%s] %s" % (getFormattedTime(), info)
		#printing_str = printing_str.encode("utf-8")
		print(printing_str)
		#if level == "warning":
		#	logging.warn(printing_str)
		#else:
		exec("logging.%s('%s')" % (level, printing_str))
	except Exception as e:
		print("[%s] Error when printing" % getFormattedTime())
		

class NewsSpider(Spider):
	def __init__(self, source_url, interested_info, max_time_interval, change_proxy_interval,
			proxy_pool_url, validate_proxy_url, headers):
		super(NewsSpider, self).__init__(max_time_interval, change_proxy_interval,
                        proxy_pool_url, validate_proxy_url, headers)
		
		self.source = source_url

		pattern = "[https?:\/\/]*[www\.]*(.*?)\.com"
		res = re.search(pattern, source_url)
		self.source_name = res.groups(0)
		#print(self.source_name)
		#input()

		self.cache_path = "articles/articles_cache/"
		self.storage_path = "articles/articles_%s/" % self.source_name
		for path in (self.cache_path, self.storage_path):
			if not os.path.exists(os.path.join(os.path.dirname(__file__), path)):
				os.mkdir(os.path.join(os.path.dirname(__file__), path))		

		self.interested_info = interested_info or []
		#self.max_num_articles = max_num_articles
		#self.interested_info_dict = {}
		#self.storage_type = "text"
		#self.storage_des = 

	def crawl(self, thread_name, article, stat, mutex_store_article, storage_type="text", storage_des=None, enable_cache=True, config_args=None):
		if config_args:
			for key in config_args:
				exec("article.config.%s = config_args['%s']" % (key, key))		
		#print(article)
		#print(type(article))
		article.download()
		if not article.html: # there may be no such an article
			printLogInfo("(%s) Article Not Exists on %s" % (thread_name, article.url), "warning")
			return 
		#print(article.title)
		#print(article.url)
		#input()
		if enable_cache:
			cache_file = codecs.open(self.cache_path + getFormattedTime(), 'w+', "utf-8")
			cache_file.write(article.html)
			cache_file.close()
		article.parse()
		info_dict = {}
		for info_name in self.interested_info:
			info_dict[info_name] = eval("article.%s"%info_name)
			if type(info_dict[info_name]) in (list, set):
				info_dict[info_name] = ','.join(info_dict[info_name])	
			elif type(info_dict[info_name]) == datetime:
				info_dict[info_name] = info_dict[info_name].strftime("%Y-%m-%d")

		# For text, storage_des is a file descriptor;
		# For database, storage_des is a database connection
		assert storage_des, "(%s) Storage destination can not be None." % thread_name
		
		mutex_store_article.acquire()
		if stat["cur_num_articles"] >= stat["max_num_articles"]: 
			# the number of articles we have got exceeds the maximum number we want.
			mutex_store_article.release()
			return 
		try:
			if storage_type == "text":
				#fi = storage_des
				try:
					fi = emptyAppendOpen(self.storage_path + article.title) #codecs.open(article.title, 'w+', "utf-8")
					fi.write(' '.join(interested_info) + '\n')
				except Exception as e:
					mutex_store_article.release()
					printLogInfo("(%s) "%thread_name + str(e), "error")
					return

				info_str = ""
				for info_name in self.interested_info:
					#if type(info_dict[info_name]) in (list, set):
					#	info_str += '&'.join(info_dict[info_name]) + '|'
					#else:
					info_str += (info_dict[info_name] + '|')
					#print(info_str)
					#input()
				info_str = info_str[:-1] + '\n'
				fi.write(info_str)
				fi.close()
			elif storage_type == "db":
				db = storage_des
				db.hset("article_contents", article.title, article.publish_date)
				db.hmset(article.title, info_dict)
			stat["cur_num_articles"] += 1
			printLogInfo("(%s) (%d/%d) Crawling and storing DONE - %s" % (thread_name, stat["cur_num_articles"], stat["max_num_articles"], article.title), "info")
			#stat["cur_num_articles"] += 1
		except Exception as e:
			printLogInfo("(%s) "%thread_name + str(e), "error")
		finally:
			mutex_store_article.release()

		#printLogInfo("(Crawling DONE) - %s" % article.title, "info")		

	def run(self, thread_name, article_pool, stat, mutex_get_article, mutex_store_article, storage_type="text", storage_des=None, enable_cache=True, config_args=None): 
		# article_pool is a queue of articles waiting for being downloaded.
		while True:
			#acticle = None
			mutex_get_article.acquire()
			try:
				if not article_pool.empty():	
					article = article_pool.get()				
				else:
					article = None
			except Exception as e:
				mutex_get_article.release()
				printLogInfo("(%s) "%thread_name + str(e), "error")
				continue

			mutex_get_article.release()

			if not article:
				printLogInfo("========== (%s) Thread END ==========" % thread_name, "info")
				return 0
			#print(article)
			#input()	
			self.crawl(thread_name, article, stat, mutex_store_article, storage_type, storage_des, enable_cache, config_args)
			time.sleep(self.max_time_interval * random.random())	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", type=int, help="the number of threads")
	parser.add_argument("-s", help="source of news")
	args = parser.parse_args()
	
	setproctitle.setproctitle("news-spider")	
	
	dirname_log = "log"
	dirname_articles = "articles"
	path_log = os.path.join(os.path.dirname(__file__), dirname_log)
	path_articles = os.path.join(os.path.dirname(__file__), dirname_articles)
	for path in (path_log, path_articles):	
		if not os.path.exists(path):
			os.mkdir(path)

	max_time_interval = 3.0
	change_proxy_interval = 10
	proxy_pool_url = "http://23.106.134.177:5010/" # url for getting proxy 
        
	# TODO: Wrong validate IP below
	validate_proxy_url = "http://104.160.39.34:9000" # url for getting current IP to validate the proxy
        
	#url_list = []
	headers = {
                "Cache-Control": "max-age=0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive"
        }
	source_url = args.s  #"https://www.cnn.com"
	interested_info = ["title", "source_url", "url", "tags", "publish_date", "authors", "summary", "text"]
	article_pool = Queue()
	stat = {"cur_num_articles": 0, "max_num_articles": float("Inf")}
	storage_type = "text"
	#storage_des = emptyAppendOpen("./article_storage")
	#storage_des.write(' '.join(interested_info) + '\n')
	storage_des = " "
	enable_cache = False
	config_args = None

	pattern = "[https?:\/\/]*[www\.]*(.*?)\.com"
	res = re.search(pattern, source_url)
	source_name = res.groups(0)
	logging.basicConfig(filename='log/news_spider_%s.log'%source_name, level=logging.INFO)	

	num_threads = args.t
	threads = []
	mutex_get_article, mutex_store_article = threading.Lock(), threading.Lock()
	
	if os.path.exists(os.path.join(os.path.dirname(__file__), "articles","articles_%s"%source_name)): # current news source has been crawled before, so just crawl the incremental articles
		memoize_articles = True
	else:
		memoize_articles = False

	fetch_images = False
	verbose = True
	news_source = newspaper.build(source_url, headers=headers, memoize_articles=memoize_articles, 
				fetch_images=fetch_images, verbose=verbose)

	stat["max_num_articles"] = min(stat["max_num_articles"], news_source.size())

	for article in news_source.articles:
		article_pool.put(article)
	
	for i in range(1, num_threads+1):
		spider = NewsSpider(source_url, interested_info, max_time_interval, change_proxy_interval,
                        proxy_pool_url, validate_proxy_url, headers)

		threads.append(threading.Thread(target=spider.run, name="NewsSpider-%d"%i, args=("NewsSpider-%d"%i, article_pool, stat, mutex_get_article, mutex_store_article, storage_type, storage_des, enable_cache, config_args)))
		
	for i in range(num_threads):
		printLogInfo("========== (%s) Start! ==========" % ("NewsSpider-%d"%(i+1)), "info")
		threads[i].start()		
		"""
		proxy = self.getValidProxy(mode=get_proxy_mode)
                while proxy == None: # No valid proxy now, sleep for invalid_proxy_interval seconds and query valid proxy again.
                        print "[Warning] No valid proxy, sleeping for %d s" % invalid_proxy_interval
                        sleep(invalid_proxy_interval)
                        proxy = self.getValidProxy(mode=get_proxy_mode)

                crawling_count = 0
                while(url != "done"): # if url == "done", it means that the crawling has finished
                        self.crawl(url, proxy)
                        self.crawlDoneConfirm(url)
                        crawling_count += 1
                        running_interval = random.random() * self.max_time_interval
                        print "[Info] URL (%s) crawlled done, sleep for %fs before the next running" % (url, running_interval)
                        sleep(running_interval)
                        url = self.getCrawlURL(mode=get_url_mode)
                        if crawling_count >= self.change_proxy_interval:
                                proxy = self.getValidProxy(mode=get_proxy_mode)
                                while proxy == None: # No valid proxy now, sleep for invalid_proxy_interval seconds and query valid proxy again.
                                        print "[Warning] No valid proxy, sleeping for %d s" % invalid_proxy_interval
                                        sleep(invalid_proxy_interval)
                                        proxy = self.getValidProxy(mode=get_proxy_mode)
                                crawling_count = 0
                print "[Info] SpiderSlave (node id: %s, slave id: %s) has done." % (self.node_id, self.slave_id)			
		"""


