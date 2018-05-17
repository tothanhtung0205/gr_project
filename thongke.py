# -*- coding=utf-8 -*-
# author = "tungtt"
from io import open

from tfidf_model import TfidfModel

SPLIT_LENGTH = 100
import os
path = os.getcwd()

# t = TfidfModel('data/train_50.txt', 'data/corpus_train_50.txt')
# t.stemming("data/stemming_corpus.txt")
#
# test_set = t.get_test_data('data/test_50.txt')
#
# count1 = 0
# count2 = 0
# with open("thongke_tfidf_stemming.txt","w",encoding="utf-8") as f:
#     for test_sen in test_set:
#
#         sim = t.get_sim(test_sen,stemming=True)
#         sim_mi = float(sim[0][2])
#         sim = u"\n\n".join([u"\n".join([sen[0],sen[1],sen[2]]) for sen in sim])
#         prced_test_sen = t.stemming_preprocess(test_sen)
#         #todo
#         if( sim_mi >= 0.6):
#             count1 += 1
#
#
#         f.write(test_sen + u"\n" +prced_test_sen+u'\n')
#         f.write( u"-" * SPLIT_LENGTH + "\n")
#         f.write(sim)
#         f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")
#         #elif(sim_mi >= 0.4):
#         #     count2 += 1
#         #     print test_sen + "\n"
#         #     print sim
#         #     print("=" * SPLIT_LENGTH)
#         # print "_"*SPLIT_LENGTH
#     f.close()
#     print("Number of sen > 0.6 : %d " %count1)
#     #print("\nNumber of sen > 0.4 : %d" % count2)


TRAIN_PATH = path + '/data/train_50.txt'
CORPUS_PATH = path + '/data/corpus_train_50_new.txt'
TEST_PATH = path + '/data/test_50.txt'

# avg_w2v_model = AvgW2vModel(TRAIN_PATH,CORPUS_PATH)
# avg_w2v_model.train()
# avg_w2v_model.get_sent2vec_matrix()
#
# test_set = avg_w2v_model.get_test_data(TEST_PATH)
tfidf_model = TfidfModel(TRAIN_PATH,CORPUS_PATH)

test_set = tfidf_model.get_test_data(TEST_PATH)

count1 = 0
count2 = 0
with open("thongke/thongke_tfidf.txt","w",encoding="utf-8") as f:
    for test_sen in test_set:

        sim =tfidf_model.get_similar_sen(test_sen,4)
        sim_mi = float(sim[0][2])
        sim = u"\n\n".join([u"\n".join([sen[0],sen[1],sen[2]]) for sen in sim])
        prced_test_sen = tfidf_model.pre_process(test_sen)
        #todo
        if( sim_mi >= 0.5):
            count1 += 1


        f.write(test_sen + u"\n" +prced_test_sen+u'\n')
        f.write( u"-" * SPLIT_LENGTH + "\n")
        f.write(sim)
        f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")
        #elif(sim_mi >= 0.4):
        #     count2 += 1
        #     print test_sen + "\n"
        #     print sim
        #     print("=" * SPLIT_LENGTH)
        # print "_"*SPLIT_LENGTH
    f.close()
    print("Number of sen > 0.5 : %d " %count1)
