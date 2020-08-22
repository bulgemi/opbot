# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import os
import pandas as pd
import matplotlib.pyplot as plt
from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer, MaxScoreTokenizer
from soynlp.vectorizer import BaseVectorizer
from soynlp.normalizer import repeat_normalize
import pickle


class Bow(object):
    def __init__(self, csv_file):
        """
        BOW(bag of words) 초기화
        :param csv_file:
        """
        self.data = pd.read_csv(csv_file)
        self.nouns = None
        self.tokenized_text = list()
        self.tokenizer = None
        self.corpus = None
        self.tok_len_list = list()

    def tokenization(self):
        """
        토큰화(tokenization)
        :return:
        """
        print(self.data.shape)
        # 장애 msg list 생성.
        msg_list = self.data.iloc[:, 1].astype(str).tolist()

        with open('message_list.txt', 'w') as f:
            for item in msg_list:
                print(item)
                f.write("%s\n\n" % item)

        corpus_path = 'message_list.txt'

        # WordExtractor 로부터 단어 점수를 학습
        self.corpus = DoublespaceLineCorpus(corpus_path, iter_sent=True)
        noun_extractor = LRNounExtractor_v2(verbose=True)
        self.nouns = noun_extractor.train_extract(self.corpus)

        print(list(noun_extractor._compounds_components.items())[:10])

        word_extractor = WordExtractor(min_frequency=100,
                                       min_cohesion_forward=0.05,
                                       min_right_branching_entropy=0.0)
        word_extractor.train(msg_list)  # list of str or like
        words = word_extractor.extract()
        cohesion_score = {word: score.cohesion_forward for word, score in words.items()}
        # tokenizer = MaxScoreTokenizer(scores=cohesion_score)
        self.tokenizer = LTokenizer(scores=cohesion_score)

        print(self.tokenizer.tokenize(msg_list[0]))
        print(msg_list[0])

        for msg in msg_list:
            self.tokenized_text.append(repeat_normalize(" ".join(self.tokenizer.tokenize(msg)), num_repeats=2))
        print(self.tokenized_text[0])

    def save_pickle(self):
        with open('data/tokenized_text.pickle', 'wb') as f:
            pickle.dump(self.tokenized_text, f, pickle.HIGHEST_PROTOCOL)

    def repeat_nor(self):
        pass

    def vectorize(self):
        vectorizer = BaseVectorizer(min_tf=1, tokenizer=self.tokenizer)
        self.corpus.iter_sent = False

        matrix_path = os.getenv('OPBOT_HOME') + 'datapreprocessor/data/vector'
        vectorizer.fit_to_file(self.corpus, matrix_path)
        # print(vectorizer.encode_a_doc_to_bow(self.tokenized_text[0]))

        for tok in self.tokenized_text:
            self.tok_len_list.append(len(vectorizer.encode_a_doc_to_list(tok)))

        print(self.tokenized_text[0])
        tmp = vectorizer.encode_a_doc_to_list(self.tokenized_text[0])
        print(tmp)
        print(vectorizer.decode_from_list(tmp))

    def visualization(self):
        """
        시각화
        :return:
        """
        plt.rcParams["font.family"] = 'NanumGothic'
        noun = list(self.nouns.keys())
        l_values = list(self.nouns.values())
        values = [frequency[0] for frequency in l_values]
        fig, axs = plt.subplots()
        axs.barh(noun[:50], values[:50])
        fig.suptitle('noun frequency')
        plt.show()

    def nor_info(self):
        print("최대 형태소 건수: %d, 편균 형태소 건수: %d" % (max(self.tok_len_list),
                                                sum(self.tok_len_list)/len(self.tok_len_list)))


if __name__ == '__main__':
    bow = Bow("data/Rims_stopword.csv")
    bow.tokenization()
    bow.save_pickle()
    bow.vectorize()
    bow.visualization()
    bow.nor_info()
