# -*- coding=utf-8 -*-
# author = "tungtt"

from data import Data

import gensim

from gensim.models.doc2vec import Doc2Vec, TaggedDocument


class Doc2vecModel(Data):
    def __init__(self,train,corpus_file):
        super(Doc2vecModel,self).__init__(train,corpus_file)

    def train(self):
        try:
            self.d2v_model = gensim.models.Doc2Vec.load('model/doc2vec.model')
            print("Load model completed!!!")
        except:
            corpus = self.corpus
            tagged_data = [TaggedDocument(words=_d.lower().split(), tags=[str(i)]) for i, _d in enumerate(corpus)]
            max_epochs = 10
            vec_size = 300
            alpha = 0.025

            model = Doc2Vec(size=vec_size,
                            alpha=alpha,
                            min_alpha=0.025,
                            min_count=5,
                            )

            model.build_vocab(tagged_data)

            for epoch in range(max_epochs):
                print('iteration {0}'.format(epoch))
                model.train(tagged_data,
                            total_examples=model.corpus_count,
                            epochs=model.iter)
                # decrease the learning rate
                model.alpha -= 0.002
                # fix the learning rate, no decay
                model.min_alpha = model.alpha

            model.save("model/doc2vec.model")
            print("Model Saved")
            self.d2v_model = model
    def get_sim(self,new_sen):
        list_sim_sen = []
        prced_sen = self.pre_process(new_sen)
        prced_sen = prced_sen.split()
        vec_new_sen = self.d2v_model.infer_vector(prced_sen)
        most_sim = self.d2v_model.docvecs.most_similar([vec_new_sen], topn=3)
        for sim_sen in most_sim:
            raw_sen = self.data[int(sim_sen[0])]
            corpus_sen =  self.corpus[int(sim_sen[0])]
            similar = sim_sen[1]
            list_sim_sen.append([raw_sen,corpus_sen,similar])
        return  list_sim_sen

if __name__ == "__main__":
    model = Doc2vecModel('data/train.txt','data/corpus_train.txt')
    model.train()
    test = model.get_sim(u"Thưa thầy cô cho em hỏi , - Cấu trúc một bài thuyết trình thường bao gồm mấy phần? Em cảm ơn thầy cô!")
    print test
