import os
import pandas as pd
from collections import Counter
from pyspark import SparkContext
import numpy as np

map_path = './uscities.csv'



def splitArticleText(article):
    return article['text'].split(' ')

def getCityName(city_row):
    return [city_row['AccentCity'], city_row['Latitude'], city_row['Longitude']] 

class mapper:
    def __init__(self, path):
	print 'ok========================================================================================================'
        self.cities = np.array(pd.read_csv(path)).tolist()
         		
    def checkCities(self, article_list):
	print 'here======================================================================================================'
	spark_context = SparkContext.getOrCreate( 'local[*]', 'demo')        
	cities = self.cities
        #freq = [0 for _ in range(cities.shape[0])]
        #references = [[] for _ in range(cities.shape[0])]
        art_rdd = spark_context.parallelize(article_list)
        city_rdd = spark_context.parallelize(self.cities)
        art_rdd = art_rdd.flatMap(splitArticleText).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
        city_rdd = city_rdd.map(getCityName).map(lambda city_info: list(city_info) + [0]))
        intersection = city_rdd.cogroup(art_rdd).filter(lambda x: x[1][0] and x[1][1])
        res_rdd = intersection.map(lambda x: (x[0], list(x[1][0]))).map(lambda (x,y): (x, y[0]))
        res = res_rdd.collect()
        #freq = [res[i][1] for i in range(len(res))]
        references = [{'title':'test%d'%i, 'url':'www.cnn.com'} for i in range(len(res))]
        return [{'AccentCity':res[i][0], 'Latitude':res[i][1], 'Longitude':res[i][2], 'References': [references[i]]} for i in range(len(res))]
        
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
