# -*- coding=utf-8 -*-
# author = "tungtt"

from flask import Flask, request , render_template
import json
from io import open
from threading import Thread
from tfidf_model import TfidfModel

model = TfidfModel('data/train_50.txt','data/corpus_train_50.txt')
app = Flask('qa')


def save_new_sen(new_sen):
    global model
    model.update(new_sen)


@app.route('/',methods = ['GET'])
def homepage():
	return render_template('home.html')


@app.route('/qa', methods=['POST'])
def process_request():
    data = request.get_data()
    handle = Thread(target=save_new_sen,args=(data,))
    handle.start()
    x = model.get_sim(data)
    if len(x) == 0:
        return "none"
    else:
        x = json.dumps(x)
        print ('Response data to client .')
        return x


if __name__ == '__main__':
    app.run(port = 8008)