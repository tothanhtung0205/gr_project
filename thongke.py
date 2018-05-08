# -*- coding=utf-8 -*-
# author = "tungtt"
from  tfidf_model import TfidfModel
from io import open
from doc2vec_model import Doc2vecModel
SPLIT_LENGTH = 100


t = TfidfModel('data/train_50.txt', 'data/corpus_train_50.txt')
t.stemming("data/stemming_corpus.txt")

test_set = t.get_test_data('data/test_50.txt')

count1 = 0
count2 = 0
with open("thongke_tfidf_stemming.txt","w",encoding="utf-8") as f:
    for test_sen in test_set:

        sim = t.get_sim(test_sen,stemming=True)
        sim_mi = float(sim[0][2])
        sim = u"\n\n".join([u"\n".join([sen[0],sen[1],sen[2]]) for sen in sim])
        prced_test_sen = t.stemming_preprocess(test_sen)
        #todo
        if( sim_mi >= 0.6):
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
    print("Number of sen > 0.6 : %d " %count1)
    #print("\nNumber of sen > 0.4 : %d" % count2)