# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression


class Ngram(object):
    def __init__(self, pickle_file):
        """
        n-gram 초기화
        :param pickle_file:
        :return:
        """
        with open(pickle_file, 'rb') as f:
            self.data = pickle.load(f)

    def do(self):
        cv = CountVectorizer(ngram_range=(1, 3)).fit(self.data)
        print("어휘 사전: %r" % cv.get_feature_names()[:10])
        print("어휘 사전 크기: %r" % len(cv.vocabulary_))


if __name__ == '__main__':
    n_gram = Ngram("data/tokenized_text.pickle")
    n_gram.do()
