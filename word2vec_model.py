# -*- coding=utf-8 -*-
# author = "tungtt"
from gensim.models import Word2Vec
from collections import Counter
from data import Data
from underthesea import word_sent
from sklearn.externals import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import os
path = os.getcwd()

class AvgW2vModel(Data):
    def __init__(self,train,corpus_file):
        super(AvgW2vModel,self).__init__(train,corpus_file)

    def train(self):
        ques_list = self.corpus
        ans_list = self.get_corpus_from_file(path+"/data/corpus_ans.txt")
        ques_list_list = [ques.split(" ") for ques in ques_list]
        ans_list_list = [ans.split(" ") for ans in ans_list]
        sens = ques_list_list + ans_list_list
        print("Training model...")
        w2v_model = Word2Vec(sens,size=100,window=5,min_count=0,workers=4)
        self.w2v_model = w2v_model

    def sen_to_vec(self,sen):
        model = self.w2v_model
        vect_sen = np.zeros(shape=(100))
        size  = len(sen)
        words= sen.split(" ")
        for word in words:
            try:
                word2vec = model[word]
            except:
                word2vec = np.zeros(shape=(100))
            vect_sen = vect_sen+word2vec
        return vect_sen/size

    def get_sent2vec_matrix(self):
        sent_vec_matrix = []
        for i,sen in enumerate(self.corpus):
            sen_vec = self.sen_to_vec(sen)
            sent_vec_matrix.append(sen_vec)
            print("Sent to vect " + str(i))
        self.sen2vec_matrix = sent_vec_matrix

    def get_new_sen_sent2vec(self,new_sen):
        new_sen = self.pre_process(new_sen)
        new_sen = new_sen.split()
        word_dict = self.w2v_model.wv.vocab
        word_dict = [key for key in word_dict]
        removed_sen = []
        for word in new_sen:
            if (word in word_dict):
                removed_sen.append(word)
        sent = " ".join(removed_sen)
        sent2vec = self.sen_to_vec(sent)
        return sent2vec


    def get_similar_sen(self,new_sen):
        data = self.data
        ans_list = self.ans_list
        corpus = self.corpus
        sent2vec_matrix = self.sen2vec_matrix

        similar_sen_list = []
        tfidf_new = self.get_new_sen_sent2vec(new_sen)
        tfidf_new = [tfidf_new]
        cos_sim = cosine_similarity(tfidf_new, sent2vec_matrix)
        cos_sim = cos_sim[0]
        for i in xrange(1):
            max_val = max(cos_sim)
            max_idx = np.where(cos_sim == max_val)
            max_idx = max_idx[0][0]
            raw_sen = data[max_idx]
            sen = corpus[max_idx]
            ans = ans_list[max_idx]
            similar_sen_list.append([raw_sen, sen, unicode(max_val), ans])
            cos_sim[max_idx] = -1
        return (similar_sen_list)
    def run(self):
        self.train()
        self.get_sent2vec_matrix()
# avg_w2v_model = AvgW2vModel('data/train.txt','data/corpus_train.txt')
# avg_w2v_model.run()
# print avg_w2v_model
# x = avg_w2v_model.get_similar_sen(u"cấu_trúc bài thuyết trình bao gồm mấy phần")
# print x