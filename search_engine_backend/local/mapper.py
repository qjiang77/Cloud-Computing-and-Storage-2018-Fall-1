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
	#print 'ok========================================================================================================'
        self.cities = np.array(pd.read_csv(path)).tolist()
         		
    def checkCities(self, article_list):
	#print 'here======================================================================================================'
	conf = SparkConf()
	conf.setMaster('local[*]').setAppName("demo")	
	#spark_context = SparkContext( 'local[*]', 'demo')        
	spark_context = SparkContext.getOrCreate()        	
	cities = self.cities
        #freq = [0 for _ in range(cities.shape[0])]
        #references = [[] for _ in range(cities.shape[0])]
        art_rdd = spark_context.parallelize(article_list)
        city_rdd = spark_context.parallelize(self.cities)
        #print city_rdd.collect()
        art_rdd = art_rdd.flatMap(splitArticleText).reduceByKey(lambda a, b: a)#map(lambda tup: (tup[0], tup[1], tup[2], 1)).reduceByKey(lambda a, b: a + b)
        city_rdd = city_rdd.map(getCityInfo)#.map(lambda city_info: list(city_info))
        #city_inters = city_rdd.cogroup(art_rdd).filter(lambda x: x[1][0] and x[1][1])
	#art_inters = art_rdd.cogroup(city_rdd).filter(lambda x: x[1][0] and x[1][1])       
	#res_rdd = intersection.map(lambda x: (x[0], list(x[1][0])))#.map(lambda (x,y): (x, y[0]))
	res_rdd = city_rdd.join(art_rdd).reduceByKey(lambda a, b: a)        
	res = res_rdd.collect()
	
	for item in res:
		print item        
	print len(res)	
	#freq = [res[i][1] for i in range(len(res))]
        references = [{'title': res[i][1][1][0], 'url':res[i][1][1][1]} for i in range(len(res))]
        return [{'AccentCity':res[i][0], 'Latitude':res[i][1][0][0], 'Longitude':res[i][1][0][1], 'References': [references[i]]} for i in range(len(res))]
        
        """
        for article in article_list:
			text = article['text']
			words = spark_context.parallelize(text.split(' '))
			count = Counter(words)
			double_words = [words[i] + ' ' + words[i + 1] for i in range(len(words) - 1)]
			double_count = Counter(double_words)

			for index, row in cities.iterrows():
				ref = False
				if row['City'] in count or row['AccentCity'] in count or row['City'] in double_count or row['AccentCity'] in double_count:
					freq[index] += 1
					references[index].append({'title': article['title'], 'url': article['url']})

		cities['Frequency'] = pd.Series(freq).values
		cities['References'] = pd.Series(references).values
		cities = cities[(cities['Frequency'] > 0)]
		#res = cities.to_dict('records')

		return cities.to_dict('records')
        """
if __name__ == '__main__':
    a = {'title': 'gainesville daily', 'url': 'www.ggg.com', 'text' : 'gainesville perfect'}
    b = {'title': 'tampa daily', 'url': 'www.ttt.com','text': 'tampa bad'}
    c = {'title': 'orlando daily', 'url': 'www.ooo.com','text': 'gainesville fantastic'}
    m = mapper(map_path)
    print(m.checkCities([a,b,c]))
