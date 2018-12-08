import os
import time
from query import Query

class Searcher:
    def __init__(self):
        self.path_article_dirs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_spider/articles")
        self.q = Query("q")

    def search(self, input_text):
        query_words = self.q.search(input_text)
        query_res = set()

        start_time = time.time()

        for subdir in os.listdir(self.path_article_dirs):
            path_files = os.path.join(self.path_article_dirs, subdir)
            for fname in os.listdir(path_files):
                path_file = os.path.join(path_files, fname)
                f = open(path_file, 'r')
                article = f.read()
                f.close()
                for wd in query_words:
                    if article.find(wd.encode('utf8')) >= 0:
                        query_res.add(fname)
            

end_time = time.time()
print query_res
print "Naive Search Time: " + str((end_time - start_time)*200) + "s"
    
    
    
