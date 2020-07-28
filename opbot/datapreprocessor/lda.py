# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pickle
import numpy as np
import mglearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


class Lda(object):
    def __init__(self, pickle_file):
        """

        :param pickle_file:
        """
        with open(pickle_file, 'rb') as f:
            self.data = pickle.load(f)
        self.sorting = None
        self.feature_names = None
        self.document_topics = None

    def do(self):
        vect = CountVectorizer(max_features=10000, max_df=.15)
        X = vect.fit_transform(self.data)
        lda = LatentDirichletAllocation(n_components=100, learning_method="batch", max_iter=25, random_state=0)
        self.document_topics = lda.fit_transform(X)
        self.sorting = np.argsort(lda.components_, axis=1)[:, ::-1]
        self.feature_names = np.array(vect.get_feature_names())

    def print_topics(self):
        mglearn.tools.print_topics(topics=range(10), feature_names=self.feature_names, sorting=self.sorting,
                                   topics_per_chunk=7, n_words=20)

    def print_barh(self):
        import matplotlib.pyplot as plt
        plt.rcParams["font.family"] = 'NanumGothic'
        fig, ax = plt.subplots(1, 2, figsize=(10, 10))
        fig.suptitle('LDA')
        topic_names = ["{:>2} ".format(i) + " ".join(words)
                       for i, words in enumerate(self.feature_names[self.sorting[:, :2]])]
        for col in [0, 1]:
            start = col * 50
            end = (col + 1) * 50
            ax[col].barh(np.arange(50), np.sum(self.document_topics, axis=0)[start:end])
            ax[col].set_yticks(np.arange(50))
            ax[col].set_yticklabels(topic_names[start:end], ha='left', va='top')
            ax[col].invert_yaxis()
            ax[col].set_xlim(0, 2000)
            yax = ax[col].get_yaxis()
            yax.set_tick_params(pad=130)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    lda = Lda("data/tokenized_text.pickle")
    lda.do()
    lda.print_topics()
    lda.print_barh()
