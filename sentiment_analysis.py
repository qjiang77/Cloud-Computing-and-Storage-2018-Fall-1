import os
from textblob import TextBlob

def sentiment_analysis(article): ### input : article text string
		analysis = TextBlob(article.decode('utf-8'))
		sentiment = analysis.sentiment.polarity ### > 0 : positive; < 0 : negative; == 0 : neutral
		polar = ''
		if sentiment > 0:
			polar = 'positive'
		elif sentiment < 0:
			polar = 'negative'
		else:
			polar = 'neutral'
		return sentiment, polar

def data_batch_analysis(article_list): ### input : list of articles from database
	res = []
	polar_res = {'positive' : 0, 'negative' : 0, 'neutral' : 0}
	
	for article in article_list:
		text = article['text']
		sentiment, polar = sentiment_analysis(text)
		res.append(sentiment)
		polar_res[polar] += 1

	return polar_res

def sentiment_analysis_from_local_file(article_path): ### input: article's path
		f = open(article_path, 'r')
		f.readline()
		return sentiment_analysis(f.read())

def batch_analysis_from_local_file(path): ### input: multiple articles' directory
	paths = []
	for name in os.listdir(path):
		paths.append(path + name)

	res = []
	polar_res = {'positive' : 0, 'negative' : 0, 'neutral' : 0}

	for p in paths:
		sentiment, polar = test(p)
		res.append(sentiment)
		polar_res[polar] += 1

	return polar_res


if __name__ == '__main__':
	a = {'text' : 'good'}
	b = {'text': 'bad'}
	print data_batch_analysis([a, b])