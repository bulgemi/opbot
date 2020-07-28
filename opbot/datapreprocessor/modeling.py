# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pickle
import pandas as pd
import mglearn
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


class Modeling(object):
    def __init__(self, pickle_file):
        self.dbscan = DBSCAN()

        with open(pickle_file, 'rb') as f:
            self.matrix = pickle.load(f)
        self.data = pd.DataFrame(self.matrix.toarray())
        self.cluster = None

    def do(self):
        self.cluster = self.dbscan.fit_predict(self.data)
        print("(%r) %r" % (len(self.cluster), self.cluster))

    def visualization(self):
        """
        시각화
        :return:
        """
        plt.rcParams["font.family"] = 'NanumGothic'
        tmp = self.data.to_numpy()
        fig, ax = plt.subplots()
        for r, v in enumerate(tmp):
            for i, iv in enumerate(v):
                if tmp[r][i] > 0:
                    ax.plot(r, i, marker='o', linestyle='')
        plt.xlabel("특성 0")
        plt.ylabel("특성 1")
        plt.show()


if __name__ == '__main__':
    md = Modeling("data/tfidf_matrix.pickle")
    md.do()
    # md.visualization()
