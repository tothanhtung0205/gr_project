# -*- coding=utf-8 -*-
# author = "tungtt"
from  tfidf_model import TfidfModel
from io import open
from doc2vec_model import Doc2vecModel
SPLIT_LENGTH = 100


t = TfidfModel('data/train.txt', 'data/corpus_train.txt')
test_set = t.get_test_data('data/test.txt')

count1 = 0
count2 = 0
with open("thongke.txt","w",encoding="utf-8") as f:
    for test_sen in test_set:

        sim = t.get_sim(test_sen)
        #sim_mi = float(sim[0][2])
        sim = u"\n\n".join([u"\n".join(sen) for sen in sim])
        # if( sim_mi >= 0.6):
        if(1):
            count1 += 1
            f.write(test_sen + u"\n" + u"-" * SPLIT_LENGTH + "\n")
            f.write(sim)
            f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")
        #elif(sim_mi >= 0.4):
            count2 += 1
            print test_sen + "\n"
            print sim
            print("=" * SPLIT_LENGTH)
        print "_"*SPLIT_LENGTH
    f.close()
    print("Number of sen > 0.6 : %d " %count1)
    print("\nNumber of sen > 0.4 : %d" % count2)