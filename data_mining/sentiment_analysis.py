import os
#import requests
from textblob import TextBlob

basepath = '/Users/jyguo/Desktop/Courses/Cloud_Computing/articles/articles_cnbc/'

def test(article_path): ### input: article's path
		f = open(article_path, 'r')
		f.readline()
		text = f.read().decode('utf-8')
		analysis = TextBlob(text)
		return analysis.sentiment.polarity ### > 0 : positive; < 0 : negative; == 0 : neutral

def sentiment_analysis(article): ### input : article string
		article = article.decode('utf-8')
		analysis = TextBlob(text)
		return analysis.sentiment.polarity ### > 0 : positive; < 0 : negative; == 0 : neutral

def batch_analysis(path): ### input: multiple articles' directory
	paths = []
	for name in os.listdir(path):
		paths.append(path + name)

	res = []
	polar_res = {'positive' : 0, 'negative' : 0, 'neutral' : 0}

	for p in paths:
		sentiment = test(p)
		polar = ''
		if sentiment > 0:
			polar = 'positive'
		elif sentiment < 0:
			polar = 'negative'
		else:
			polar = 'neutral'
		
		res.append(sentiment)
		polar_res[polar] += 1

	return polar_res


if __name__ == '__main__':
	'''
	for filename in os.listdir(basepath):
			newname = filename.replace(',', '')
			newname = newname.replace(':', '')
			os.rename(basepath+filename, basepath+newname)
	'''
	print batch_analysis(basepath)


'''
sentiment_url = 'http://text-processing.com/api/sentiment/'
headers = {'content-type': 'application/sentiment', 'Accept-Charset': 'UTF-8'}


def sentiment_analysis(article_path):
		f = open(article_path, 'r')
		f.readline()
		text = f.read().split('|')[-1]
		data = {'text': text}
		r_json = None
		try:
			r_json = requests.post(sentiment_url, data = data, headers = headers).json()
		except:
			pass
		return (r_json['probability']['neg'], r_json['probability']['pos']) if r_json else None
'''