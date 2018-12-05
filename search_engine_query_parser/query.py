import preprocessor

class Query:
    def __init__(self, name):
        """ Init Query with its name """
        self.name = name

    def searchExecute(self):
        p = preprocessor.Preprocessor("p")
        text = p.getSearchContent()
        res = p.executePre(text)
        print res
        return res


if __name__ == '__main__':
    q = Query("q")
    q.searchExecute()