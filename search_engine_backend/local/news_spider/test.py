import newspaper

cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)

for article in cnn_paper.articles:
    print(article.url)

for category in cnn_paper.category_urls():
    print(category)

cnn_article = cnn_paper.articles[0]
print(cnn_article.config.memoize_articles)
cnn_article.download()
print(cnn_article.title)
input()
print(cnn_article.html.encode("utf-8"))
cnn_article.parse()
