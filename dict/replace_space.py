# -*- coding=utf-8 -*-
# author = "tungtt"

from io import open

with open('syndict_eg020.txt',"r",encoding="utf-8") as f:
    with open('final_syndict.txt',"w",encoding="utf-8") as f_w:
        for line in f:
            line = line.replace(" ","_")
            line = line.replace("==","\t")
            f_w.write(line)
    f_w.close()