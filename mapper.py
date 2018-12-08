import os
import pandas as pd
from collections import Counter
from pyspark import SparkContext
from pyspark.conf import SparkConf
import numpy as np

map_path = './uscities.csv'



def splitArticleText(article):
    return [(word, (article['title'], article['url'])) for word in article['text'].split(' ')]  

def getCityInfo(city_row):
    return (city_row[2], (city_row[5], city_row[6]))

class mapper:
    def __init__(self, path):
        self.cities = np.array(pd.read_csv(path)).tolist()
         		
    def checkCities(self, article_list):
	conf = SparkConf()
	conf.setMaster('local[*]').setAppName("demo")	        
	spark_context = SparkContext.getOrCreate()        	
	cities = self.cities
        art_rdd = spark_context.parallelize(article_list)
        city_rdd = spark_context.parallelize(self.cities)
        art_rdd = art_rdd.flatMap(splitArticleText).reduceByKey(lambda a, b: a)
        city_rdd = city_rdd.map(getCityInfo)

	res_rdd = city_rdd.join(art_rdd).reduceByKey(lambda a, b: a)        
	res = res_rdd.collect()
	
	for item in res:
		print item        
	print len(res)	
        references = [{'title': res[i][1][1][0], 'url':res[i][1][1][1]} for i in range(len(res))]
        return [{'AccentCity':res[i][0], 'Latitude':res[i][1][0][0], 'Longitude':res[i][1][0][1], 'References': [references[i]]} for i in range(len(res))]
        

if __name__ == '__main__':
    a = {'title': 'gainesville daily', 'url': 'www.ggg.com', 'text' : 'gainesville perfect'}
    b = {'title': 'tampa daily', 'url': 'www.ttt.com','text': 'tampa bad'}
    c = {'title': 'orlando daily', 'url': 'www.ooo.com','text': 'gainesville fantastic'}
    m = mapper(map_path)
    print(m.checkCities([a,b,c]))
