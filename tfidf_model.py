# -*- coding=utf-8 -*-
# author = "tungtt"
from time import time
from data import Data
import numpy as np
from io import open
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_sent
from collections import Counter
from sklearn.externals import joblib
from sklearn.cluster import KMeans

class TfidfModel(Data):

    def __init__(self,train,corpus_file,clustering = False):
        super(TfidfModel,self).__init__(train,corpus_file)
        self.vect = TfidfVectorizer()
        t0 = time()
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)
        print("Calculate tfidf in %f s" %(time() - t0) )
        self.cluster_or_not = clustering
        if clustering == True:
            self.clustering()

    def update(self,new_sen,new_ans):
        """
        add new_sen to corpus and re-calculate corpus_tfidf_matrix
        :param new_sen:
        :return:
        """

        self.data.append(new_sen)
        new_prced_sen = self.pre_process(new_sen)
        self.corpus.append(new_prced_sen)
        self.ans_list.append(new_ans)
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)
        print("Updated new sentences from file")


    def write_dict(self,file_name):
        """
        Write word dictionary to file_name
        :param file_name: filename to write
        :return:
        """
        dict = self.vect.get_feature_names()
        with open(file_name,"w",encoding="utf-8") as f_w:
            for word in dict:
                f_w.write(word)
                f_w.write(u'\n')
        f_w.close()


    def get_new_sen_tfidf(self,new_sen,vect):
        """
        preprocess new_sen , remove word that not exist in dictionary
        Calculate TFIDF of new sentence
        :param new_sen:
        :return: tfidf_vec of new_sen
        """
        new_sen = self.pre_process(new_sen)
        new_sen = new_sen.split()
        dict = vect.get_feature_names()
        idf = vect.idf_
        removed_sen = []
        for word in new_sen:
            if (word in dict):
                removed_sen.append(word)
        tf = Counter(removed_sen)
        tf_vect = [0] * len(dict)
        for i, word in enumerate(dict):
            if word in removed_sen:
                x = tf[word]
                tf_vect[i] = x
        tfidf_vec = [a * b for a, b in zip(tf_vect, idf)]
        return tfidf_vec


    def get_similar_sen(self,new_sen,num_sens):
        """
        get 4 similar sen in corpus of new_sen
        :param new_sen:
               num_sens : number of similar sens
        :return: list of 4 similar sentences with new_sen
         element of list : [raw_sen,corpus_sen,cosine,answer]
        """



        # todo getclust()
        if self.cluster_or_not == True:
            clust = self.get_cluster(new_sen)
            tfidf_matrix = self.clusters_list[clust]["tfidf_matrix"]
            data = self.clusters_list[clust]["data"]
            ans_list = self.clusters_list[clust]["ans_list"]
            corpus = self.clusters_list[clust]["corpus"]
            vect = self.clusters_list[clust]["vect"]
            print("Get data from clust %d" %clust)

        else:
            tfidf_matrix = self.corpus_tfidf_matrix
            data = self.data
            ans_list = self.ans_list
            corpus = self.corpus
            vect = self.vect

        similar_sen_list = []
        tfidf_new = self.get_new_sen_tfidf(new_sen,vect)
        tfidf_new = [tfidf_new]
        t0 = time()
        cos_sim = cosine_similarity(tfidf_new, tfidf_matrix)
        print("Calculate cosine similar in %f s" %(time()-t0))
        cos_sim = cos_sim[0]
        for i in xrange(num_sens):
            max_val = max(cos_sim)
            max_idx = np.where(cos_sim == max_val)
            max_idx = max_idx[0][0]
            raw_sen = data[max_idx]
            sen = corpus[max_idx]
            ans = ans_list[max_idx]
            similar_sen_list.append([raw_sen, sen, unicode(max_val), ans])
            cos_sim[max_idx] = -1
        return (similar_sen_list)


    def get_sim(self,new_sen):
        """
        get 4 similar sens with new_sen
        :param new_sen:
        :return: list of similar sen that cosine > 0.4
        """
        sen_list = self.get_similar_sen(new_sen,3)
        arr = []
        for sen in sen_list:
            if float(sen[2]) > 0.6:
                arr.append([sen[0],sen[3]])
        # return [[sen[0],sen[3]] for sen in sen_list]
        print arr
        return arr

    #clustering
    def clustering(self):
        try:
            self.centers = joblib.load("centers.bin")
            self.clusters_list = joblib.load("clusters_list.bin")
            print("Get K-means from file")
            for i,clust in enumerate(self.clusters_list):
                self.clusters_list[i]["vect"] = TfidfVectorizer()
                self.clusters_list[i]["tfidf_matrix"]   =   self.clusters_list[i]["vect"].fit_transform(clust["corpus"])
        except:
            k = 4
            km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
            tfidf_matrix = self.corpus_tfidf_matrix
            t0 = time()
            km.fit(tfidf_matrix)
            print("Clustering time %f" %(time()-t0))
            clusters = km.predict(tfidf_matrix)
            self.centers = km.cluster_centers_
            joblib.dump(self.centers, "centers.bin")


            f = []
            for j in xrange(0,k):
                a = {"data":[],"corpus":[],"ans_list":[]}
                f.append(a)
            for i,clust in enumerate(clusters):
                f[clust]["data"].append(self.data[i])
                f[clust]["corpus"].append(self.corpus[i])
                f[clust]["ans_list"].append(self.ans_list[i])

            self.clusters_list = f
            joblib.dump(self.clusters_list,"clusters_list.bin")


    def get_cluster(self,new_sen):
        centers = self.centers
        tfidf = self.get_new_sen_tfidf(new_sen,self.vect)
        tfidf = [tfidf]
        cos_sim = cosine_similarity(tfidf,centers)
        cos_sim = cos_sim[0]
        max_val = max(cos_sim)
        max_idx = np.where(cos_sim == max_val)
        vlue = max_idx[0][0]
        return vlue

if __name__ == "__main__":
    model = TfidfModel('data/train.txt','data/corpus_train.txt',clustering=True)
    test = model.get_similar_sen(u"cấu trúc bài thuyết trình gồm mấy phần",4)
    test = model.get_similar_sen(u"Đàm phán cứng và đàm phán mềm khác nhau thế nào", 4)
    test = model.get_similar_sen(u"Cho em hỏi khi nào nộp bài tập", 4)
    test = model.get_similar_sen(u"Thưa thầy cô cho em hỏi : Kỹ năng thuyết phục là gì vậy. Em cảm ơn thầy cô!",4)
    print test