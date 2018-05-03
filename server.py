# -*- coding=utf-8 -*-
# author = "tungtt"

from flask import Flask, request , render_template
import json
from io import open

from tfidf_model import TfidfModel


model = TfidfModel('data/train.txt','data/corpus_train.txt')
#model = Model(tfidf.TRAIN,tfidf.TOKENIZED_TRAIN)
app = Flask('qa')

@app.route('/',methods = ['GET'])
def homepage():
	return render_template('gr_ui.html')

@app.route('/qa', methods=['POST'])
def process_request():
    data = request.get_data()
    x = model.get_sim(data)
    x = json.dumps(x)
    return x

if __name__ == '__main__':
    app.run(port = 8008)
