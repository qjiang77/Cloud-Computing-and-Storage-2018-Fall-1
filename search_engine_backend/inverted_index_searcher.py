import time
from pyspark import SparkContext
from pyspark.sql import SparkSession 
from pyspark.sql import SQLContext 
from query import Query

class InvertedIndexSearcher:
    def __init__(self):
        self.spark_session = SparkSession.builder.getOrCreate()
        self.database = SQLContext(self.spark_session) 
        self.df = self.database.read.format("jdbc").options(
            url="jdbc:mysql://localhost:3306/course_cloud_computing_18fall?serverTimezone=UTC", 
            driver="com.mysql.jdbc.Driver", 
            dbtable="inverted_index",
            user="root", 
            password="root").load()
    
    def search(self, query_words):
        docs = set()
        for wd in query_words:
            query_res = set()
            for row in self.df.select('*').where('word = "%s"' % wd.lower()).collect():
                query_res = query_res.union(set(row["doc"].split('|')))
            docs = docs.union(query_res) 
        return docs

if __name__ == "__main__":
    searcher = InvertedIndexSearcher()
    q = Query("q")
    query_words = q.searchExecute()

    start_time = time.time()
    print searcher.search(query_words)
    end_time = time.time()
    print "Spark Search Time: " + str(end_time - start_time) + "s"