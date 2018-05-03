# -*- coding=utf-8 -*-
# author = "tungtt"

from data import Data
import numpy as np
from io import open
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_sent
from collections import Counter

class TfidfModel(Data):
    def __init__(self,train,corpus_file):
        super(TfidfModel,self).__init__(train,corpus_file)
        self.vect = TfidfVectorizer()
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)

    def get_new_sen_tfidf(self,new_sen):
        new_sen = self.pre_process(new_sen)
        new_sen = new_sen.split()
        dict = self.vect.get_feature_names()
        idf = self.vect.idf_
        removed_sen = []
        for word in new_sen:
            if (word in dict):
                removed_sen.append(word)
        tf = Counter(removed_sen)
        tf_vect = [0] * len(dict)
        for i, word in enumerate(dict):
            if word in removed_sen:
                x = tf[word]
                y = len(removed_sen)
                tf_vect[i] = x
        tfidf_vec = [a * b for a, b in zip(tf_vect, idf)]
        return tfidf_vec

    def get_similar_sen(self,new_sen):
        tfidf_matrix = self.corpus_tfidf_matrix
        data = self.data
        ans_list = self.ans_list
        corpus = self.corpus

        similar_sen_list = []
        tfidf_new = self.get_new_sen_tfidf(new_sen)
        tfidf_new = [tfidf_new]
        cos_sim = cosine_similarity(tfidf_new, tfidf_matrix)
        cos_sim = cos_sim[0]
        for i in xrange(4):
            max_val = max(cos_sim)
            max_idx = np.where(cos_sim == max_val)
            max_idx = max_idx[0][0]
            raw_sen = data[max_idx]
            sen = corpus[max_idx]
            ans = ans_list[max_idx]
            # similar_sen_list.append(raw_sen+u"\n"+sen+u"\n" + unicode(max_val))
            similar_sen_list.append([raw_sen, sen, unicode(max_val), ans])
            cos_sim[max_idx] = -1
        # return "\n\n".join(similar_sen_list)
        return (similar_sen_list)

    def get_sim(self,new_sen):
        sen_list = self.get_similar_sen(new_sen)
        arr = []
        for sen in sen_list:
            if float(sen[2]) < 0.6:
                sen[0] = u"Không có câu hỏi nào tương tự"
                sen[3] = u"Hệ thống chưa trả lời đc câu hỏi này!"
            arr.append([sen[0],sen[3]])
        # return [[sen[0],sen[3]] for sen in sen_list]
        print arr
        return arr


# t = TfidfModel('data/train.txt','data/corpus_train.txt')
# dict = t.vect.get_feature_names()
# print dict

