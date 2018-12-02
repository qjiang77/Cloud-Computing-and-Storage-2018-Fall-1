import os
import pandas as pd
from collections import Counter

map_path = './uscities.csv'

class mapper:
	def __init__(self, path):
		self.cities = pd.read_csv(path)
		
	def checkCities(self, article_list):
		whole_text = ' '.join([article['text'] for article in article_list])

		words = whole_text.split(' ')
		count = Counter(words)
		double_words = [words[i] + ' ' + words[i + 1] for i in range(len(words) - 1)]
		double_count = Counter(double_words)
		
		cities = self.cities

		freq = [0] * cities.shape[0]
		
		for index, row in cities.iterrows():
			if row['City'] in count:
				freq[index] += count[row['City']]
			if row['AccentCity'] in count:
				freq[index] += count[row['AccentCity']]
			if row['City'] in double_count:
				freq[index] += double_count[row['City']]
			if row['AccentCity'] in double_count:
				freq[index] += double_count[row['AccentCity']]
		
		cities['Frequency'] = pd.Series(freq).values
		cities = cities[(cities['Frequency'] > 0)]
		return cities.to_dict('records')

if __name__ == '__main__':
	a = {'text' : 'gainesville good'}
	b = {'text': 'tampa bad'}
	m = mapper(map_path)
	print(m.checkCities([a,b]))