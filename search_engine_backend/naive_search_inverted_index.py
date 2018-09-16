import os
import time
from query import Query

path_articles = "/home/blackfrog/Documents/Cloud Computing/news_spider/articles/articles_cnn"

q = Query("q")
query_words = q.searchExecute()

query_res = set()

start_time = time.time()

for fname in os.listdir(path_articles):
    path_file = os.path.join(path_articles, fname)
    f = open(path_file, 'r')
    article = f.read()
    f.close()
    for wd in query_words:
        if article.find(wd.encode('utf8')) >= 0:
            query_res.add(fname)
            

end_time = time.time()
print query_res
print "Naive Search Time: " + str((end_time - start_time)*200) + "s"
    
    
    