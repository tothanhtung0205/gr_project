# -*- coding=utf-8 -*-
# author = "tungtt"
from scipy import sparse
import pandas as pd
import numpy as np
from io import open
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_sent
from collections import Counter



def read_data(file_name):
    dataset = []
    with open(file_name,"r",encoding="utf-8") as f:
        for line in f:
            ques = line.split("\t")[2]
            dataset.append(ques)
    return dataset


def get_stw_list():
    stw_list = []
    with open("dict/stopwords.txt","r",encoding="utf-8") as f:
        for line in f:
            line = line.replace("\n","")
            stw_list.append(line)
    return stw_list


def remove_stw(sen,stw_list):
    words_list = []
    words = sen.split(" ")
    for word in words:
        if word in stw_list:
            continue
        else:
            words_list.append(word)
    return " ".join(words_list)


def pre_process(stw_list,data):
    corpus = []
    for sen in data:
        sen = word_sent(sen,format="text")
        sen =  repace_wrong_tokenize(sen)
        prced_sen = remove_stw(sen,stw_list)
        corpus.append(prced_sen)
    return corpus



def get_corpus(stw_list,file_name):
    corpus = []
    with open(file_name,"r",encoding="utf-8") as f:
        for line in f:
            line = line.lower()
            line = line.replace(u"\n","")
            line = remove_stw(line,stw_list)
            corpus.append(line)
    return corpus



def get_dictionary(data):
    vect = TfidfVectorizer()
    tfidf_matrix = vect.fit_transform(corpus)
    dict = vect.get_feature_names()
    a = vect.idf_
    idf_map = zip(a, dict)
    idf_sorted = sorted(idf_map, key=lambda x: x[0])
    with open("dict/dict.txt", "w", encoding="utf-8") as f:
        for word in idf_sorted:
            f.write(word[1])
            f.write(u"\n")

    f.close()


def get_new_sen_tfidf(new_sen, vect,stw_list):
    new_sen = new_sen.lower()
    new_sen = pre_process(stw_list,[new_sen])[0]
    new_sen = new_sen.split()
    dict = vect.get_feature_names()
    idf = vect.idf_
    removed_sen = []
    for word in new_sen:
        if(word in dict):
            removed_sen.append(word)
    print " ".join(removed_sen)
    print("=========================================")
    tf = Counter(removed_sen)
    #max_w = max(tf,key=tf.get)
    #max_tf = tf[max_w]
    tf_vect = [0]*len(dict)
    for i,word in enumerate(dict):
        if word in removed_sen:
            x = tf[word]
            y = len(removed_sen)
            tf_vect[i] = x/y
    # print("tf_vector ============================")
    # print sparse.csr_matrix(tf_vect)
    tfidf_vec = [a * b for a, b in zip(tf_vect, idf)]
    # print sparse.csr_matrix(tfidf_vec)
    # print("=================================\n")
    return tfidf_vec


def get_similar_sen(new_sen,data,corpus,tfidf_matrix):

    similar_sen_list = []
    tfidf_new = get_new_sen_tfidf(new_sen, vect,stw_list)
    tfidf_new = [tfidf_new]
    cos_sim = cosine_similarity(tfidf_new, tfidf_matrix)
    cos_sim = cos_sim[0]
    for i in xrange(3):
        max_val = max(cos_sim)
        max_idx = np.where(cos_sim == max_val)
        max_idx = max_idx[0][0]
        raw_sen = data[max_idx]
        sen = corpus[max_idx]
        similar_sen_list.append(raw_sen+u"\n"+sen+u"\n" + unicode(max_val))
        cos_sim[max_idx] = -1
    return "\n\n".join(similar_sen_list)


def repace_wrong_tokenize(sen):
    #todo tao file replace
    sen = sen.replace(u"bài tập",u"bài_tập")
    sen = sen.replace(u"học tập",u"học_tập")
    sen = sen.replace(u"ko",u"không")
    sen = sen.replace(u"kỷ năng",u"kỹ_năng")
    sen = sen.replace(u"biểu hiện",u"biểu_hiện")
    sen = sen.replace(u"thành công_của",u"thành_công của")
    sen = sen.replace(u"học_tập trung",u"học tập_trung")
    for c in sen:
        if c in [u"-",u"?",u"!",u",",u";",u".",u":",u'/']:
            sen = sen.replace(c,u" ")
    return sen

def write_data(data,to_write):
    count = 0
    with open(to_write,"w",encoding="utf-8") as f_w:
        for sen in data:
            count+=1
            print("Write sentence %d" %count)
            sen = word_sent(sen,format="text")
            sen = repace_wrong_tokenize(sen)
            f_w.write(sen)
            f_w.write(u"\n")
    f_w.close()

def get_test_data(file_name):
    test_list = []
    with open(file_name,"r",encoding="utf-8") as f_r:
        for line in f_r:
            sen = line.split("\t")[2]
            test_list.append(sen)
    return test_list

if __name__ == '__main__':
    data = read_data("data/train.txt")
    #write_data(data,"data/tokenized_train.txt")
    stw_list = get_stw_list()
    corpus = get_corpus(stw_list,"data/tokenized_train.txt")
    vect = TfidfVectorizer()
    corpus_tfidf_matrix = vect.fit_transform(corpus)

    test_set = get_test_data("data/test.txt")
    for test_sen in test_set:
        print test_sen
        sim = get_similar_sen(test_sen,data,corpus,corpus_tfidf_matrix)
        print sim
        print("\n===========================================")
        i =raw_input("continue?")
        if (i=='0'):
            break


