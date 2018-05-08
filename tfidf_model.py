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


    def update(self,new_sen):
        self.data.append(new_sen)
        new_prced_sen = self.pre_process(new_sen)
        self.corpus.append(new_prced_sen)
        self.ans_list.append(new_prced_sen)
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)
        print("Updated new sentence from file")
        #print("Write new sentence to file")

    def stemming_preprocess(self,new_sen):
        sen = word_sent(new_sen, format="text")
        sen = sen.lower()
        sen = self.repace_wrong_tokenize(sen)
        prced_sen = self.remove_stw(sen)
        syndict = self.get_syndict()
        prced_sen = self.replace_syn_sen(prced_sen,syndict)
        return prced_sen


    def get_new_sen_tfidf(self,new_sen,stemming):
        if stemming == True:
            new_sen = self.stemming_preprocess(new_sen)
            #todo sua o day
        else:
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


    def get_similar_sen(self,new_sen,stemming):
        tfidf_matrix = self.corpus_tfidf_matrix
        data = self.data
        ans_list = self.ans_list
        corpus = self.corpus

        similar_sen_list = []
        tfidf_new = self.get_new_sen_tfidf(new_sen,stemming)
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


    def get_sim(self,new_sen,stemming):
        sen_list = self.get_similar_sen(new_sen,stemming)
        arr = []
        for sen in sen_list:
            # if float(sen[2]) < 0.6:
            #     sen[0] = u"Không có câu hỏi nào tương tự"
            #     sen[3] = u"Hệ thống chưa trả lời đc câu hỏi này!"
            arr.append(sen)
        # return [[sen[0],sen[3]] for sen in sen_list]
        print arr
        return arr

    def write_dict(self,file_name):
        dict = self.vect.get_feature_names()
        with open(file_name,"w",encoding="utf-8") as f_w:
            for word in dict:
                f_w.write(word)
                f_w.write(u'\n')
        f_w.close()

    # for stemming synonym
    def get_syndict(self):

        syndict = []
        with open('dict/final_syndict.txt',"r",encoding="utf-8") as f:
            for line in f:
                line = line.replace("\n","")
                arr = line.split("\t")
                syndict.append(arr)
        print("Got syndict from file")
        return syndict

    def replace_syn(self,word,syndict):
        represent = word
        for line in syndict:
            if word in line:
                represent = line[0]
                print("Replace " + word +" with " +represent)
                break
        return represent

    def replace_syn_sen(self,sen,syndict):
        sen = sen.replace("\n", "")
        sen = sen.split()
        for i, word in enumerate(sen):
            sen[i] = self.replace_syn(word, syndict)
        stemming_sen = u" ".join(sen)
        return stemming_sen

    def get_stemming_corpus(self,corpus_file):
        syndict = self.get_syndict()
        corpus = self.corpus
        steming_corpus = []
        count = 0
        with open(corpus_file,"w",encoding="utf-8") as f_w:
            for sen in corpus:
                stemming_sen = self.replace_syn_sen(sen,syndict)
                f_w.write(stemming_sen)
                f_w.write(u"\n")
                count+=1
                print("Write sent %d" %count)
                steming_corpus.append(stemming_sen)
            f_w.close()
        return steming_corpus


    def stemming(self,corpus_file):
        stemming_corpus = []
        try:
            print("Get stemming corpus from file.")
            with open(corpus_file, "r", encoding="utf-8") as f:
                for line in f:
                    stemming_corpus.append(line)
        except:
            print("Get steming corpus from data and write to file .")
            stemming_corpus = self.get_stemming_corpus(corpus_file)
        self.corpus = stemming_corpus
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)


model = TfidfModel('data/train_50.txt','data/corpus_train_50.txt')
model.stemming("data/stemming_corpus.txt")
model.write_dict('dict/dict_after_stemming.txt')

