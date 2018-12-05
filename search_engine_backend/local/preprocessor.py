from nltk.corpus import wordnet, stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class Preprocessor:
    def __init__(self, name):
        """ Init Preprocessor with its name """
        self.name = name

    def getSearchContent(self):
        """ Get the search text user tap """
        text = raw_input("Search Content: ")
        return text


    def executePre(self, text):
        """
        :param text: A search content the user tap on keyboard
        :return: An array with several synonyms of the key words from search content
        """
        # tokenize sentences to words
        word_tokens = word_tokenize(text)

        # filter stopwords
        stop_words = set(stopwords.words('english'))
        filterd_sentence = [w for w in word_tokens if not w in stop_words]

        # generate synonyms words
        synonyms = []
        for filter_word in filterd_sentence:
            synonyms.append(filter_word)
            for syn in wordnet.synsets(filter_word):
                for l in syn.lemmas():
                    synonyms.append(l.name())
        return synonyms