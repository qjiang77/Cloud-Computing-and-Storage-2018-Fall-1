import os
import tornado.ioloop
from tornado.web import RequestHandler
import torndb

class article:
    def __init__(self):
        self.title = "Test"
        self.content = "This is a test article"
        self.publish_date = "Oct 20, 2018"

class MainHandler(RequestHandler):
    def get(self):
        self.render("static/index.html")

class InvertedIndexHandler(RequestHandler):
    def get(self, word):
        db = torndb.Connection("localhost", "news", "root", "root") 
        query_res = db.query("SELECT * FROM inverted_index where word = '%s'" % word)
        #print type(query_res)
        if not query_res:
            self.write("Word '%s' not found" % word)
        else:
            res = ""
            docs = query_res[0]['doc'].split('|')
            for doc in docs:
                res += doc + '\n'
            self.write(res)

class ArticleListHandler(RequestHandler):
    def get(self):
        art = article()
        args = {
            "articles": [art]
        }
        self.render("static/blog-list.html", **args)

def make_app():
    url_handlers = [
        (r"/", MainHandler),
        (r"/inverted-index/(.+)", InvertedIndexHandler),
        (r"/article-list", ArticleListHandler)
    ]

    settings = {
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static") 
    }
    #template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
    #print template_path

    return tornado.web.Application(url_handlers, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
