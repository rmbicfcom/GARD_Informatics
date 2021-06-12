#
# coding latin-1

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

fname = "gardid.tsv"
df = pd.read_csv(fname, sep="\t", encoding='iso-8859-1')
df['ID'] = df.apply(lambda x: str(int(x['DiseaseID'].replace("GARD:", ""))), axis=1)
#print(df)
baseURL = "https://rarediseases.info.nih.gov/diseases/"
suffURL = "/disease"

#myurl = "https://rarediseases.info.nih.gov/diseases/2088/ehlers-danlos-syndrome-classic-type"
cols = ['GARD_Disease_ID', 'DiseaseID', 'ID', 'DiseaseName', 'URL', 'Title', 'MetaDescription']
print("\t".join(cols))
for i in df.index: # head(10).index:
    myurl = "".join([baseURL, df['ID'][i], suffURL])
    #print(myurl)
    data = []
    data.append(df['GARD_Disease_ID'][i])
    data.append(df['DiseaseID'][i])
    data.append(df['ID'][i])
    data.append(df['DiseaseName'][i])
    data.append(myurl)
    response = requests.get(myurl)
    #print (response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    mytags = soup.findAll('meta')
    
    metadesc = soup.find("meta", attrs={"name": "description"})
    desc = metadesc['content'].replace("\n", " ").replace("\t", " ").strip() if metadesc else "No meta description"
    data.append(desc)
    #print(desc)
    pagetitle = soup.find("title")
    title = pagetitle.text.replace("\n", " ").replace("\t", " ").strip() if pagetitle else "No title"
    data.append(title)
    print("\t".join(data))
    time.sleep(1)



