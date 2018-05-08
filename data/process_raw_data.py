import pandas as pd
from io import open
from bs4 import BeautifulSoup

def replace_space(text):
    text = " ".join(text.split())
    return text

def read_data():
    dataset = []
    df = pd.read_csv("EG020.csv",encoding="utf-8")
    a = df.values
    for row in a:
        col2 = BeautifulSoup(row[2]).text
        col2 = replace_space(col2)
        row[2] = col2
        col3 = BeautifulSoup(row[3]).text
        row[3] = replace_space(col3)
        line = u"\t".join(row)
        dataset.append(line)
    return dataset

data = read_data()
with open("raw_EG020.txt","w",encoding="utf-8") as f:
    for elm in data:
        f.write(elm)
        f.write(u"\n")
    f.close()

