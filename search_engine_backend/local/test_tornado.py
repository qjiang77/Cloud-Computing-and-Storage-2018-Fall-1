import os
import tornado.ioloop
from tornado.web import RequestHandler
import torndb
from inverted_index_searcher import InvertedIndexSearcher
from query import Query
from mapper import *
from sentiment_analysis import data_batch_analysis


search_res = set()


class Article:
    def __init__(self, title, text, publish_date, url, max_display_len):
        self.max_display_len = max_display_len
        self.title = title
        self.text = text[:self.max_display_len]
        self.publish_date = publish_date
        self.url = url


class MainHandler(RequestHandler):
    def get(self):
        self.render("static/index.html")


"""
def searchInvIndex(words):
    docs = set()
    db = torndb.Connection("localhost", "news", "root", "root")
    for word in words:
        query_res = db.query("SELECT * FROM inverted_index where word = '%s'" % word)
        #print type(query_res)
        if not query_res:
            continue
        else:
            docs = docs.union(set(query_res[0]['doc'].split('|')))
    return docs
"""


class InvertedIndexHandler(RequestHandler):
    def get(self, word):
        db = torndb.Connection("localhost", "news", "root", "root")
        query_res = db.query("SELECT * FROM inverted_index where word = '%s'" % word)
        # print type(query_res)
        if not query_res:
            self.write("Word '%s' not found" % word)
        else:
            res = ""
            docs = query_res[0]['doc'].split('|')
            for doc in docs:
                res += doc + '\n'
            self.write(res)


class SearchHandler(RequestHandler):
    def fetchArticles(self, article_titles):
        """
        print article_titles
        path_article_dirs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_spider/articles")
        articles = []
        for subdir in os.listdir(path_article_dirs):
            path_subdir = os.path.join(path_article_dirs, subdir)
            for fname in os.listdir(path_subdir):
                if fname in article_titles:
                    try:
                        f = open(os.path.join(path_subdir, fname), 'r')
                        print os.path.join(path_subdir, fname), len(f.readlines())
                        sections = f.readlines()[0].split('|')
                        items = ''.join(f.readlines()[1:]).split('|')
                        art = Article(
                                title = items[sections.index('title')],
                                text = items[sections.index('text')],
                                publish_date = items[sections.index('publish_date')],
                                url = items[sections.index('url')]
                            )
                        articles.append(art)
                    except Exception as e:
                        print str(e)
                        continue
        return articles
        """
        articles = set()
        db = torndb.Connection("localhost", "news", "root", "root")
        for title in article_titles:
            # print title
            query_res = db.query("SELECT * FROM article where title = '%s'" % title)
            if query_res:
                art = Article(
                    title=query_res[0]['title'].replace('_', ' '),
                    text=query_res[0]['text'],
                    publish_date=query_res[0]['publish_date'],
                    url=query_res[0]['url'],
                    max_display_len=300
                )
                articles.add(art)
        global search_res
        search_res = articles
        return articles

    def get(self):
        # art = article()
        # path_article_dirs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_spider/articles")

        input_text = self.get_query_argument(name="search")
        # print input_text
        q = Query("q")
        # print input_text
        query_words = q.search(input_text)
        # print query_words
        # print query_words
        searcher = InvertedIndexSearcher()
        article_titles = searcher.search(query_words)
        # print article_titles

        args = {
            "articles": self.fetchArticles(article_titles),
            "input_text": input_text
        }
        # print args
        self.render("static/blog-list.html", **args)


class MapHandler(RequestHandler):
    
    def fetchArticles(self, article_titles):
        """
        print article_titles
        path_article_dirs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_spider/articles")
        articles = []
        for subdir in os.listdir(path_article_dirs):
            path_subdir = os.path.join(path_article_dirs, subdir)
            for fname in os.listdir(path_subdir):
                if fname in article_titles:
                    try:
                        f = open(os.path.join(path_subdir, fname), 'r')
                        print os.path.join(path_subdir, fname), len(f.readlines())
                        sections = f.readlines()[0].split('|')
                        items = ''.join(f.readlines()[1:]).split('|')
                        art = Article(
                                title = items[sections.index('title')],
                                text = items[sections.index('text')],
                                publish_date = items[sections.index('publish_date')],
                                url = items[sections.index('url')]
                            )
                        articles.append(art)
                    except Exception as e:
                        print str(e)
                        continue
        return articles
        """
        articles = set()
        db = torndb.Connection("localhost", "news", "root", "root")
        for title in article_titles:
            # print title
            query_res = db.query("SELECT * FROM article where title = '%s'" % title)
            if query_res:
                art = Article(
                    title=query_res[0]['title'].replace('_', ' '),
                    text=query_res[0]['text'],
                    publish_date=query_res[0]['publish_date'],
                    url=query_res[0]['url'],
                    max_display_len=300
                )
                articles.add(art)
        #global search_res
        #search_res = articles
        return articles

    def get(self):
	"""
        input_text = self.get_query_argument(name="search")
        q = Query("q")
        query_words = q.search(input_text)
        print query_words
        searcher = InvertedIndexSearcher()
        article_titles = searcher.search(query_words)
	searcher.stopSpark()
        print article_titles
        map0 = mapper('./uscities.csv')
        article_list = self.fetchArticles(article_titles)
        """

        global search_res
        article_list = search_res
        map_list = []
        for article in article_list:
            article_map = {}
            article_map["title"] = article.title
            article_map["text"] = article.text
            article_map["publish_date"] = article.publish_date
            article_map["url"] = article.url
            article_map["max_display_len"] = article.max_display_len
            map_list.append(article_map)
        map0 = mapper('./uscities.csv')
	#print 'there---------------------------------------------------------------------------------------------------'
	#print dir(map0)
        city_dic = map0.checkCities(map_list)
	#for item in city_dic:	
	#	print item
        self.render("static/map.html", cities=city_dic)

class ChartHandler(RequestHandler):
    def get(self):
        global search_res
        article_list = search_res
        chart_list = []
        for article in article_list:
            article_chart = {}
            article_chart["title"] = article.title
            article_chart["text"] = article.text
            article_chart["public_date"] = article.publish_date
            article_chart["url"] = article.url
            article_chart["max_display_len"] = article.max_display_len
            chart_list.append(article_chart)
        polar_res = data_batch_analysis(chart_list)

        self.render("static/chart.html", polar_res=polar_res)


def make_app():
    url_handlers = [
        (r"/", MainHandler),
        (r"/inverted-index/(.+)", InvertedIndexHandler),
        (r"/article-list", SearchHandler),
        (r"/map", MapHandler),
        (r"/chart", ChartHandler)
    ]

    settings = {
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    }
    # template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
    # print template_path

    return tornado.web.Application(url_handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
