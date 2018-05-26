# -*- coding=utf-8 -*-
# author = "tungtt"
from io import open
from time import time
from data import Data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from tfidf_model import TfidfModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.externals import joblib

class Cluster(TfidfModel):

    def __init__(self,train,corpus_file,stemming = False):
        super(Cluster,self).__init__(train,corpus_file,stemming)

        self.cluster()
        print("Finish cluster!!!")
    def cluster(self):
        k=4
        km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
        tfidf_matrix = self.corpus_tfidf_matrix
        t0 = time()
        km.fit(tfidf_matrix)
        print("Clustering time %f s" %(time()-t0))
        clusters = km.predict(tfidf_matrix)
        self.centers = km.cluster_centers_
        #joblib.dump(self.centers,"centers.bin")
        print(km.cluster_centers_)
        f = []
        for j in xrange(0,k):
            f_w = open("clust/"+str(j)+".txt","w",encoding="utf-8")
            f.append(f_w)

        for i, clush in enumerate(clusters):


            f[clush].write(self.data[i])
            f[clush].write(u"\n")
        for j in xrange(0, k):
            f[j].close()

    def get_cluster(self,new_sen):
        centers = self.centers
        tfidf = self.get_new_sen_tfidf(new_sen,vect=self.vect)
        tfidf = [tfidf]
        cos_sim = cosine_similarity(tfidf,centers)
        cos_sim = cos_sim[0]
        max_val = max(cos_sim)
        max_idx = np.where(cos_sim == max_val)
        return max_idx





cluster = Cluster("data/train.txt","data/corpus_train.txt")
clust = cluster.get_cluster(u"abcacc")



# print  cluster.get_cluster(u"Cấu trúc bài thuyết trình có mấy phần")
# print cluster.get_cluster(u"có mấy cách đàm phán")
# print cluster.get_cluster(u"bài tập này có khó ko")
# print cluster.get_cluster(u"Điểm tổng kết tính như thế nào")


