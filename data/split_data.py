from io import open

aaa = []
with open("train.txt","r",encoding="utf-8") as f:
    for line in f:
       line = line.split('--->')[0]
       aaa.append(line)


with open("created_test_2.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[:50]:
        f_w.write(sen)
        f_w.write(u'\n')
    f_w.close()


# with open("train.txt","w",encoding="utf-8") as f_w:
#     for sen in aaa[50:]:
#         f_w.write(sen)
#     f_w.close()