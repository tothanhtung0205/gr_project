# -*- coding=utf-8 -*-
# author = "tungtt"
import tfidf
class Model():
    def __init__(self):
        self.data,self.ans_list = tfidf.read_data(tfidf.TRAIN)
        # write_data(data,TOKENIZED_TRAIN)
        self.stw_list = tfidf.get_stw_list()
        self.corpus = tfidf.get_corpus(self.stw_list, tfidf.TOKENIZED_TRAIN)
        self.vect = tfidf.TfidfVectorizer()
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)

    def get_sim(self,new_sen):
        sen_list = tfidf.get_similar_sen(new_sen, self.data, self.corpus, self.corpus_tfidf_matrix, self.vect, self.stw_list,self.ans_list)
        return [[sen[0],sen[3]] for sen in sen_list]


