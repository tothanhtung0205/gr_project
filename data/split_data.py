from io import open

aaa = []
with open("qa_eg020.txt","r",encoding="utf-8") as f:
    for line in f:
       aaa.append(line)


with open("test_50.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[:50]:
        f_w.write(sen)
    f_w.close()


with open("train_50.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[50:]:
        f_w.write(sen)
    f_w.close()