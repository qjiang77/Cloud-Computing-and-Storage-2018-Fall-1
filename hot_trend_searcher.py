import time
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from query import Query


class HotTrendSearcher:
    def __init__(self):
        self.spark_session = SparkSession.builder.getOrCreate()
        self.database = SQLContext(self.spark_session)
        self.df = self.database.read.format("jdbc").options(
            url="jdbc:mysql://localhost:3306/news?serverTimezone=UTC",
            driver="com.mysql.jdbc.Driver",
            dbtable="inverted_index",
            user="root",
            password="19951029").load()

    def search(self):
        query_res = set()
        max = 0
        doc = ""
        for row in self.df.select('*').collect():
            count = len(set((row["doc"].split('|'))))
            if count > max:
                max = count
                doc = row["doc"]


        query_res = query_res.union(set(doc.split('|')))
        return query_res