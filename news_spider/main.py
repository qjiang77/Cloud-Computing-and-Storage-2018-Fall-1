import argparse
import newspaper
import os
import re
import sys
from setproctitle import setproctitle

if __name__ == "__main__":
	setproctitle("main_spider")
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int, help="the maximum number of news sources we will crawl")
	parser.add_argument('-t', type=int, help="the number of threads")
	args = parser.parse_args()
	
	source_urls = newspaper.popular_urls()
	pattern = "[https?:\/\/]*[www\.]*(.*?)\..*"

	#print(source_urls)
	for i in range(args.n):
		#print(source_urls[i])
		res = re.search(pattern, source_urls[i])
		#print(res.groups())
		source_name = res.groups(0)[0]
		#print(source_name)
		#input()
		os.system("nohup python3 news_spider.py -t %d -s %s > log/nohup_%s.out &" % (args.t, source_urls[i], source_name))

		
