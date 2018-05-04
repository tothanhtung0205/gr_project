# -*- coding=utf-8 -*-
# author = "tungtt"

from flask import Flask, request , render_template
import json
from io import open
from threading import Thread
from tfidf_model import TfidfModel

model = TfidfModel('data/train.txt','data/corpus_train.txt')
app = Flask('qa')
test_sen = "aaa"



def save_new_sen(new_sen):
    global model
    #new_sen = unicode(new_sen, "utf-8")
    model.update(new_sen)
    # print "save..."
    # print new_sen
    # with open('temp.txt',"a",encoding="utf-8") as f:
    #     f.write(new_sen)
    #     f.write(u'\n')
    # f.close()


# @app.route('/update', methods = ['GET'])
# def update():
#     global  test_sen
#     global model
#     model.update('temp.txt')
#     print "updated"
#     return "updated"

@app.route('/',methods = ['GET'])
def homepage():
	return render_template('gr_ui.html')


@app.route('/qa', methods=['POST'])
def process_request():
    data = request.get_data()
    handle = Thread(target=save_new_sen,args=(data,))
    handle.start()
    x = model.get_sim(data)
    x = json.dumps(x)
    print ('Response data to client .')
    return x


if __name__ == '__main__':
    app.run(port = 8008)
