import os
from pyspark import SparkContext
from pyspark.sql import SparkSession 
from pyspark.sql import SQLContext 
from pyspark.sql.types import *
	 
# 1. Create RDD to process the articles to get inverted index
# 2. convert RDD to DataFrame
# 3. save the DataFrame to MySQL
path_articles = "/home/blackfrog/Documents/Cloud Computing/news_spider/articles"
spark_context = SparkContext( 'local[*]', 'demo')


def parseArticle(line, headers):
    if line in headers:
        return []
    new_line = line.replace(',', '').replace(':', '').replace(';', '') \
                .replace('"', '').replace('?', '').replace('!', '').split(' ')
    try:
        new_line.remove('')
    except:
        pass
    
    return new_line

articles = []
failure_count = 0
for subdir in os.listdir(path_articles):
    
    if subdir != "articles_cnn":
        continue
    
    path_subdir = os.path.join(path_articles, subdir)
    if not os.path.isdir(path_subdir):
        continue
    for filename in os.listdir(path_subdir):
        try:
            path_file = os.path.join(path_subdir, filename.replace(',', ''))
        
            article = spark_context.textFile(path_file)
            headers = article.take(2) # For our ease, now we just ignore the meta info of an article and only focus on its content
            article = article.flatMap(lambda line: parseArticle(line, headers))\
                                .map(lambda word: (word.lower(), filename))\
                                .distinct()
                                
            article.collect() # Do not know why, but here must use an action operation.

            articles.append(article)
        except:
            failure_count += 1
            continue
    
print "Failures: " + str(failure_count)

articles = spark_context.union(articles).distinct()\
                                        .mapValues(lambda filename: [filename])\
                                        .reduceByKey(lambda filename1, filename2: filename1 + filename2)\
                                        .mapValues(lambda filenames: '|'.join(filenames))

articles.collect()
articles.cache()

spark_session = SparkSession.builder.getOrCreate()

database = SQLContext(spark_session) 

'''
df = database.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/course_cloud_computing_18fall?serverTimezone=UTC", 
    driver="com.mysql.jdbc.Driver", 
    dbtable="inverted_index",
    user="root", 
    password="root").load()
'''

schemaString = "word doc"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
df_inverted_indices = database.createDataFrame(articles, schema)
df_inverted_indices.write.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/course_cloud_computing_18fall?serverTimezone=UTC", 
    driver="com.mysql.jdbc.Driver", 
    dbtable="inverted_index",
    user="root", 
    password="root").mode('append').save()

print "Inverted index saved successfully."