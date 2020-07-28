# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TfIdf(object):
    def __init__(self, pickle_file):
        """
        tf-idf 초기화.
        :param pickle_file:
        """
        with open(pickle_file, 'rb') as f:
            self.data = pickle.load(f)
        self.tfidf_matrix = None

    def do(self):
        """
        tf-idf 처리.
        :return:
        """
        tfidf_vectorizer = TfidfVectorizer(min_df=10)
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.data)
        text = tfidf_vectorizer.get_feature_names()
        idf = tfidf_vectorizer.idf_
        print("text(%r): %r" % (len(text), text))
        print("idf(%r): %r" % (len(idf), idf))

    def save(self):
        """
        save matrix
        :return:
        """
        with open('data/tfidf_matrix.pickle', 'wb') as f:
            pickle.dump(self.tfidf_matrix, f, pickle.HIGHEST_PROTOCOL)

    def similarity(self, index):
        """
        cosine_similarity
        :param index:
        :return:
        """
        for i, r in enumerate(self.data):
            similarity = cosine_similarity(self.tfidf_matrix[index], self.tfidf_matrix[i])[0][0]

            if similarity > 0.80:
                print("similarity: ", similarity)
                print(self.data[index])
                print(self.data[i])


if __name__ == '__main__':
    tf_idf = TfIdf("data/tokenized_text.pickle")
    tf_idf.do()
    tf_idf.similarity(2578)
    tf_idf.save()
