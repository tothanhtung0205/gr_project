# -*- coding=utf-8 -*-
# author = "tungtt"

from io import open
data = []
with open("raw_EG020.txt","r",encoding="utf-8") as f:
    for line in f:
        ques = line.split("\t")
        data.append([ques[2],ques[3]])


def check_similar2(elm,data):
    ques = elm[0]
    for elm2 in data:
        ques2 = elm2[0]
        if ques2 == ques:
            print("duplicate sentence ")
            print ques
            print ques2
            return True
    return False

direct_list = []
for elm in data:
    if check_similar2(elm,direct_list):
        continue
    else:
        direct_list.append(elm)

with open("EG020.txt","w",encoding="utf-8") as f_w:
    for line in direct_list:
        line = u"\t".join(line)
        f_w.write(line)
    f_w.close()
