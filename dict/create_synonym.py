# -*- coding=utf-8 -*-
# author = "tungtt"

from io import open
import glob
from sklearn.externals import joblib

sym_dict = []
files = glob.glob("vi-wordnet/*.csv")
for file in files:
    with open(file,"r",encoding="utf-8") as f:
        for line in f:
            line = line.replace("\n","")
            word = line.split(", ")
            if len(word) == 1:
                continue
            else:
                sym_dict.append(word)

# with open('synonym_dict.txt',"r",encoding="utf-8") as f_r:
#     for line in f_r:
#         line = line.replace("\n","")
#         line = line.split(', ')
#         sym_dict.append(line)
#
# print sym_dict

try:
    dict = joblib.load("syndict.bin")
except:
    dict = []
    with open("nomed_dict.txt","r",encoding="utf-8") as read_words:
        for word in read_words:
            word = word.replace('\n',"")
            word = word.replace('_'," ")
            for line in sym_dict:
                if word in line:
                    dict.append(line)
    joblib.dump(dict,"syndict.bin")

new_dict = []
for line in dict:
    a = 0
    a_set = set(line)
    for i,line1 in enumerate(new_dict):
        b_set = set(line1)
        if (a_set & b_set):
            if len(line) > len(line1):
                new_dict[i] = line
            a = 1
            break
    if(a == 0):
        new_dict.append(line)

print new_dict



with open('syndict_eg020.txt',"w",encoding="utf-8") as f_w:
    for line in new_dict:
        line = u"==".join(line)
        f_w.write(line)
        f_w.write(u"\n")
    f_w.close()

