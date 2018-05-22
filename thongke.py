# -*- coding=utf-8 -*-
# author = "tungtt"
from io import open

from tfidf_model import TfidfModel
from word2vec_model import AvgW2vModel
SPLIT_LENGTH = 100
import os
path = os.getcwd()

TRAIN_PATH = path + '/data/train.txt'
CORPUS_PATH = path + '/data/corpus_train.txt'


def tfidf_test(test_file,result_file):
    tfidf_model = TfidfModel(TRAIN_PATH,CORPUS_PATH)
    test_set = tfidf_model.get_test_data(test_file)
    count1 = 0
    count2 = 0
    count3 = 0
    with open(result_file,"w",encoding="utf-8") as f:
        for test_sen in test_set:

            sim =tfidf_model.get_similar_sen(test_sen,1)
            sim_mi = float(sim[0][2])
            sim = u"\n\n".join([u"\n".join([sen[0],sen[1],sen[2]]) for sen in sim])
            prced_test_sen = tfidf_model.pre_process(test_sen)
            #todo
            if( sim_mi >= 0.4):
                count1 += 1
            if(sim_mi >= 0.5):
                count2 += 1

            if(sim_mi >= 0.6):
                count3 +=1
            f.write(test_sen + u"\n" + prced_test_sen + u'\n')
            f.write(u"-" * SPLIT_LENGTH + "\n")
            f.write(sim)
            f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")

        f.close()
        print("Number of sen > 0.4 : %d " % count1)
        print("Number of sen > 0.5 : %d " % count2)
        print("Number of sen > 0.6 : %d " % count3)



def w2v_avg_test(test_file , result_file):
    avg_w2v_model = AvgW2vModel(TRAIN_PATH,CORPUS_PATH)
    avg_w2v_model.train()
    avg_w2v_model.get_sent2vec_matrix()


    test_set = avg_w2v_model.get_test_data(test_file)
    with open(result_file, "w", encoding="utf-8") as f:
        for test_sen in test_set:
            sim = avg_w2v_model.get_similar_sen(test_sen)
            sim_mi = float(sim[0][2])
            sim = u"\n\n".join([u"\n".join([sen[0], sen[1], sen[2]]) for sen in sim])
            prced_test_sen =avg_w2v_model.pre_process(test_sen)
            f.write(test_sen + u"\n" + prced_test_sen + u'\n')
            f.write(u"-" * SPLIT_LENGTH + "\n")
            f.write(sim)
            f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")
        f.close()

# tfidf_test("data/","test")
w2v_avg_test("data/test_50.txt","thongke/w2v_test_50.txt")