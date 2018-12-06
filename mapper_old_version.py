import os
import pandas as pd
from collections import Counter

map_path = './uscities.csv'

class mapper:
	def __init__(self, path):
		self.cities = pd.read_csv(path)
		
	def checkCities(self, article_list):
		cities = self.cities
		freq = [0 for _ in range(cities.shape[0])]
		references = [[] for _ in range(cities.shape[0])]
		for article in article_list:
			text = article['text']
			words = text.split(' ')
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

if __name__ == '__main__':
	a = {'title': 'gainesville daily', 'url': 'www.ggg.com', 'text' : 'gainesville perfect'}
	b = {'title': 'tampa daily', 'url': 'www.ttt.com','text': 'tampa bad'}
	c = {'title': 'orlando daily', 'url': 'www.ooo.com','text': 'gainesville fantastic'}
	m = mapper(map_path)
	print(m.checkCities([a,b,c]))