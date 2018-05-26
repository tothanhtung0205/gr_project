# -*- coding=utf-8 -*-
# author = "tungtt"
from io import open
from tfidf_model import TfidfModel
from word2vec_model import AvgW2vModel
SPLIT_LENGTH = 100

TRAIN_PATH = 'data/train.txt'

def tfidf_test(tfidf_model,test_file,result_file):
    test_set = tfidf_model.get_test_data(test_file)
    count1 = 0
    count2 = 0
    count3 = 0
    with open(result_file,"w",encoding="utf-8") as f:
        for test_sen in test_set:

            sim =tfidf_model.get_similar_sen(test_sen,1)
            sim_mi = float(sim[0][2])
            sim_sen = sim[0]

            sim = u"\n".join([sim_sen[0],sim_sen[1],sim_sen[2]])
            prced_test_sen = tfidf_model.pre_process(test_sen)
            #todo
            if( sim_mi >= 0.4):
                count1 += 1
            if sim_mi >= 0.5:
                count2 += 1

            if(sim_mi >= 0.6):
                count3 +=1

            f.write(test_sen + u"\n" + prced_test_sen + u'\n')
            # clust = sim_sen[4]
            # f.write(u"Cluster %d \n" %clust)
            f.write(u"-" * SPLIT_LENGTH + "\n")
            f.write(sim)

            f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")

        f.close()
        print("Number of sen > 0.4 : %d " % count1)
        print("Number of sen > 0.5 : %d " % count2)
        print("Number of sen > 0.6 : %d " % count3)


def w2v_avg_test(corpus_file , test_file , result_file):
    avg_w2v_model = AvgW2vModel(TRAIN_PATH,corpus_file)
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


if __name__ == "__main__":
    pass
    # w2v_avg_test("data/corpus_train.txt","data/test_created.txt","thongke/w2v_created.txt")
    # tfidf = TfidfModel("data/train.txt","data/corpus_train.txt")
    # tfidf_test(tfidf,"data/test.txt","thongke/tfidf_test_50.txt")

