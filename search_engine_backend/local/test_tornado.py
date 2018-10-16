import tornado.ioloop
from tornado.web import RequestHandler
import torndb

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

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

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/inverted-index/(.+)", InvertedIndexHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
