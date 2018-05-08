# -*- coding=utf-8 -*-
# author = "tungtt"

from io import open

with open('EG020.txt',"r",encoding="utf-8") as f_r:
    with open('qa_eg020.txt',"w",encoding="utf-8") as f_w:
        for line in f_r:
            line = line.split('\t')
            line = u'--->'.join([line[2],line[3]])
            f_w.write(line)
        f_w.close()

# with open('qa_eg020.txt','r',encoding="utf-8") as f_r:
#     for line in f_r:
#         line = line.split('\t')
#         print line