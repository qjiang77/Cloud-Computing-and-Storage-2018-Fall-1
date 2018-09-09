import random
import requests 
from bs4 import BeautifulSoup as BS
from time import sleep

class Spider:
	"""
	time_interval: crawling time interval
	change_proxy_interval: change proxy for every change_proxy_interval times of crawling
	proxy_pool_url: url for getting proxy
	validate_proxy_url: url for check our IP address
	""" 
	def __init__(self, max_time_interval, change_proxy_interval, 
			proxy_pool_url, validate_proxy_url, headers):
		self.max_time_interval = max_time_interval
		self.change_proxy_interval = change_proxy_interval 
		self.proxy_pool_url = proxy_pool_url
		self.validate_proxy_url = validate_proxy_url
		self.headers = headers
	"""
	get a proxy from master HTTP server 
	return: proxy url in form {"http":"http://ip:port"}
	"""
	def __getProxyFromWeb(self):
		return {"http":"http://" + requests.get(self.proxy_pool_url).text}
	
	"""
	get a proxy from local database, normally the local database is part of a redis cluster
	"""
	def __getProxyFromDB(self):
		# TODO
		pass
	
	"""
	Interface for getting a proxy
	mode: can be either "from_web" or "from_db", determine where we get the proxy
	return: proxy url in form {"http":"http://ip:port"}
	"""
	def getProxy(self, mode="from_web"):
		assert mode in ("from_web", "from_db")
		if mode == "from_web":
			return self.__getProxyFromWeb()
		if mode == "from_db":
			return self.__getProxyFromDB()

	"""
	check if a proxy is available
	proxy: proxy url in form {"http":"http://ip:port"}
	return: bool values
	"""
	def validateProxy(self, proxy):
		# Check if we can connect to the Internet through this proxy 
		new_ip = None
		try:
			new_ip = requests.get(self.validate_proxy_url, timeout=3, proxy=proxy)
		except requests.exceptions.Timeout:
			return False
		except Exception as e:
			print(str(e))
			return False
		# Check if our real ip address is hidden by this proxy
		# That is, if our ip with proxy the same as that without proxy
		return (new_ip and new_ip != requests.get(self.validate_proxy_url, timeout=3).text) 
	
	"""
	Get a proxy and validate it. If it is invalid, repeat getting and validating until getting a valid proxy.
	If a proxy is invalid, we either send a message to proxy pool server to delete it (mode="from_web") 
				      or delete it directly in our local redis database node (mode="from_db")
	
	mode: "from_web" or "from_db"
	max_try_times: the maximum times of trying. If after this many times of trying the proxy is still invalid, abort.
	return: if finally get a valid proxy, return it in form {"http":"http://ip:port"}; 
		otherwise, return None
	"""
	def getValidProxy(self, mode="from_web", max_try_times=10):
		for i in range(max_try_times):
			proxy = self.getProxy(mode)
			if (self.validateProxy(proxy)):
				return proxy
		return None


	"""
	crawl content, needed to be overwritten
	"""
	def crawl(self, url, proxy):
		pass	
	
	"""
	waiting for multi-threading 
	"""
	def run(self):
		pass


"""
SpiderMaster: Get the number of pages and assign them to different slaves.
"""
class SpiderMaster(Spider):
	def __init__(self, max_time_interval, change_proxy_interval,
                        proxy_pool_url, validate_proxy_url, headers):
                super(SpiderMaster, self).__init__(max_time_interval, change_proxy_interval,
                                                        proxy_pool_url, validate_proxy_url, headers)
	"""
	Specific crawling process
	For specific spider, only need to overwrite this function
	"""
	def crawl(self, url, proxy=None):
		pass
		
	def run(self):
		self.crawl(url, None)

"""
SpiderSlave: Crawl content in each page
"""
class SpiderSlave(Spider):

	# TODO: Using configure file to initialize

	def __init__(self, slave_id, max_time_interval, change_proxy_interval, 
			master_url, proxy_pool_url, validate_proxy_url, headers):
		super(SpiderSlave, self).__init__(max_time_interval, change_proxy_interval, 
							proxy_pool_url, validate_proxy_url, headers)
		
		node_id_file = open("node_id.txt", "r")
		self.node_id = node_id_file.readline().replace('\n', '')
		node_id_file.close()

		if slave_id != None:
			self.slave_id = slave_id
		else:
			slave_id_file = open("slave_id.txt", "r+")
			line = slave_id_file.readline()
			if line == "": # This is a new and empty file
				self.slave_id = "1"
			else: # Not a new file, read directly
				self.slave_id = line.replace('\n', '')
			slave_id_file.close()
			slave_id_file = open("slave_id.txt", "w")
			slave_id_file.write(str(int(self.slave_id) + 1))
			slave_id_file.close()
				
		self.master_url = master_url

	"""
	Get the URL to be crawlled from HTTP server where the master spider located in
	return: URL string 
	"""
	def __getCrawlURLFromWeb(self):
		return requests.get(self.master_url).text

	"""
	Get the URL to be crawlled from local database, normally the local database is part of a redis cluster
	"""
	def __getCrawlURLFromDB(self):
		#TODO
		pass
	
	"""
	Interface for getting a URL to be crawlled
        mode: can be either "from_web" or "from_db", determine where we get the URL
        return: URL string
	"""
	def getCrawlURL(self, mode="from_web"):
		assert mode in ("from_web", "from_db")
		if mode == "from_web":
			return self.__getCrawlURLFromWeb()
		if mode == "from_db":
			return self.__getCrawlURLFromDB()
	
	"""
	Specific crawling process
	For specific spider, only need to overwrite this function
	"""
	def crawl(self, url, proxy):
		pass

	"""
	Send confirmation message to master spider that specific URL has been crawlled successfully  
	"""
	def crawlDoneConfirm(self, url):
		requests.post(self.master_url, data={"node_id":self.node_id, "slave_id":self.slave_id, "url":url, "status":"200"})

	def run(self, get_proxy_mode="from_web", get_url_mode="from_web", invalid_proxy_interval=3):
		url = self.getCrawlURL(mode=get_url_mode)
		proxy = self.getValidProxy(mode=get_proxy_mode)
		while proxy == None: # No valid proxy now, sleep for invalid_proxy_interval seconds and query valid proxy again.
			print("[Warning] No valid proxy, sleeping for %d s" % invalid_proxy_interval)
			sleep(invalid_proxy_interval)
			proxy = self.getValidProxy(mode=get_proxy_mode)
		
		crawling_count = 0
		while(url != "done"): # if url == "done", it means that the crawling has finished
			self.crawl(url, proxy)
			self.crawlDoneConfirm(url)
			crawling_count += 1
			running_interval = random.random() * self.max_time_interval
			print ("[Info] URL (%s) crawlled done, sleep for %fs before the next running" % (url, running_interval))
			sleep(running_interval)
			url = self.getCrawlURL(mode=get_url_mode)
			if crawling_count >= self.change_proxy_interval:
				proxy = self.getValidProxy(mode=get_proxy_mode)
				while proxy == None: # No valid proxy now, sleep for invalid_proxy_interval seconds and query valid proxy again.
					print ("[Warning] No valid proxy, sleeping for %d s" % invalid_proxy_interval)
					sleep(invalid_proxy_interval)
					proxy = self.getValidProxy(mode=get_proxy_mode)
				crawling_count = 0
		print ("[Info] SpiderSlave (node id: %s, slave id: %s) has done." % (self.node_id, self.slave_id))		


class SpiderMaster1point3acre(SpiderMaster):
	def __init__(self, max_time_interval, change_proxy_interval,
			proxy_pool_url, validate_proxy_url, headers, url_list):
		super(SpiderMaster1point3acre, self).__init__(max_time_interval, change_proxy_interval,
								proxy_pool_url, validate_proxy_url, headers)
		self.url_list = url_list

	def crawl(self, url="http://www.1point3acres.com/bbs/forum-198-1.html", proxy=None):
		html = requests.get(url, headers=self.headers, proxies=proxy).text
		dom = BS(html)
		last_page_urls = dom.find_all("a", class_="last")
		num_pages = int(last_page_urls[0].split('&')[-1].split('=')[-1])
		for i in range(1, num_pages+1):
			self.url_list.append(url[:-(url[::-1].find('-'))] + str(i) + '.html')

if __name__ == "__main__":

	max_time_interval = 5.0
	change_proxy_interval = 1
	proxy_pool_url = "http://104.160.39.34:5010" # url for getting proxy 
	validate_proxy_url = "http://104.160.39.34:9000" # url for getting current IP to validate the proxy
	url_list = []
	headers = {
		"Cache-Control": "max-age=0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-GB,en;q=0.5",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
		"Upgrade-Insecure-Requests": "1",
		"Connection": "keep-alive",
		"Host": "www.1point3acres.com"	
	}
	master = SpiderMaster1point3acre(max_time_interval, change_proxy_interval,
					proxy_pool_url, validate_proxy_url, headers, url_list) 
		
