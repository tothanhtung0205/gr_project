from io import open
import random

aaa = []
with open("EG020.txt","r",encoding="utf-8") as f:
    for line in f:
       aaa.append(line)

#random.shuffle(aaa)

with open("test_100.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[:100]:
        f_w.write(sen)
    f_w.close()


with open("train_100.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[100:]:
        f_w.write(sen)
    f_w.close()