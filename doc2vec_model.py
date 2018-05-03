# -*- coding=utf-8 -*-
# author = "tungtt"

from model import Model
import tfidf
import gensim

from gensim.models.doc2vec import Doc2Vec, TaggedDocument


# TRAIN = 'data/EG020.txt'
# TOKED_TRAIN = 'data/tokenized_full.txt'

data_model = Model(tfidf.TRAIN,tfidf.TOKENIZED_TRAIN)
corpus = data_model.corpus
data = data_model.data
size = len(corpus)

tagged_data = [TaggedDocument(words=_d.lower().split(), tags=[str(i)]) for i, _d in enumerate(corpus)]

try:
    d2v_model = gensim.models.Doc2Vec.load('doc2vec.model')
    print("Load model completed!!!")
except:
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

    model.save("doc2vec.model")
    print("Model Saved")
    d2v_model = model

# print d2v_model
#
# while(1):
#     x = raw_input(u"nhap tu vao:")
#     sim_word = d2v_model.most_similar(x)
#     print sim_word
#     if x=='q':
#         break


test = tfidf.get_test_data(tfidf.TEST);
for test_sen in test:
    print '_'*100
    print test_sen
    test_sen_2 = tfidf.pre_process(data_model.stw_list,[test_sen.lower()])[0]
    print test_sen_2
    print '-'*100
    test_sen_2 = test_sen_2.split()
    new_vec_sen = d2v_model.infer_vector(test_sen_2)
    most_sim = d2v_model.docvecs.most_similar([new_vec_sen],topn=3)
    print most_sim
    for sim_sen in most_sim:
        print data[int(sim_sen[0])]
        print corpus[int(sim_sen[0])]
        print [sim_sen[1]]
        print '\n\n'
