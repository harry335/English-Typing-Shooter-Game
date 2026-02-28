import json 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from tqdm import tqdm, trange
def bbb(n):
    nn=3
    am=100
    if n=='physics':
        link='https://sheethub.com/data.gov.tw/%E5%9C%8B%E5%AE%B6%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E9%99%A2-%E7%89%A9%E7%90%86%E5%AD%B8%E5%90%8D%E8%A9%9E-%E9%AB%98%E4%B8%AD%E5%90%AB%E4%BB%A5%E4%B8%8B%E7%89%A9%E7%90%86%E5%AD%B8%E5%AD%B8%E8%A1%93%E5%90%8D%E8%A9%9E'
    elif n=='math':
        link='https://sheethub.com/data.gov.tw/%E5%9C%8B%E5%AE%B6%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E9%99%A2-%E6%95%B8%E5%AD%B8%E5%90%8D%E8%A9%9E-%E9%AB%98%E4%B8%AD%E5%90%AB%E4%BB%A5%E4%B8%8B%E6%95%B8%E5%AD%B8%E5%AD%B8%E8%A1%93%E5%90%8D%E8%A9%9E'
    elif n=='chemical':
        link='https://sheethub.com/data.gov.tw/%E5%9C%8B%E5%AE%B6%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E9%99%A2-%E5%8C%96%E5%AD%B8%E5%90%8D%E8%A9%9E-%E9%AB%98%E4%B8%AD%E4%BB%A5%E4%B8%8B%E5%8C%96%E5%AD%B8%E5%90%8D%E8%A9%9E'
    elif n=='biology':
        link='https://sheethub.com/data.gov.tw/%E5%9C%8B%E5%AE%B6%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E9%99%A2-%E7%94%9F%E5%91%BD%E7%A7%91%E5%AD%B8%E5%AD%B8%E8%A1%93%E5%90%8D%E8%A9%9E'
        nn=4
    Hbiol=[]
    Mbiol=[]
    Ebiol=[]
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    lp=soup.find_all('li')
    page=int(lp[-10].text[-3:])
    progress = tqdm(total=3*am)
    while len(Hbiol)<am or len(Mbiol)<am or len(Ebiol)<am:
        progress.update(1)
        bio=[]
        nl=[]
        ra=random.randint(1,page)
        lk=link+'?page='+str(ra)
        r = requests.get(lk)
        soup = BeautifulSoup(r.text, 'html.parser')
        l=soup.find_all('td')
        for i in range(1,len(l)):
            l[i]=l[i].text[25:]
        nl=l[1:]
        for i in range(0,len(nl),nn):
            bio.append(nl[i].strip())
        for i in range(3):
            rrr=random.randint(0,len(bio)-1)
            if len(bio[rrr])>9 and len(bio[rrr])<=13 and len(Hbiol)<am:
                Hbiol.append(bio[rrr])
            elif len(bio[rrr])<=9 and len(bio[rrr])>6 and len(Mbiol)<am:
                Mbiol.append(bio[rrr])
            elif len(bio[rrr])<=6 and len(Ebiol)<am and bio[rrr]!='?':
                Ebiol.append(bio[rrr])   
    #單字難度分級
    easy=[]
    medium=[]
    hard=[]
    for i in  Hbiol:
        if len(i)<=5 and i.isalpha():
            i=i.lower()
            easy.append(i)
        elif 5<len(i)<=10 and i.isalpha():
            i=i.lower()
            medium.append(i)

        elif len(i)>10 and i.isalpha():
            i=i.lower()
            hard.append(i)

    for i in  Mbiol:
        if len(i)<=5 and i.isalpha():
            i=i.lower()
            easy.append(i)
        elif 5<len(i)<=10 and i.isalpha():
            i=i.lower()
            medium.append(i)

        elif len(i)>10 and i.isalpha():
            i=i.lower()
            hard.append(i)

    for i in  Ebiol:
        if len(i)<=5 and i.isalpha():
            i=i.lower()
            easy.append(i)
        elif 5<len(i)<=10 and i.isalpha():
            i=i.lower()
            medium.append(i)

        elif len(i)>10 and i.isalpha():
            i=i.lower()
            hard.append(i)

    with open ("library.txt","a") as f:
        f.write(n)
        f.write(f"{easy}")
        f.write("%")
        f.write(f"{medium}")
        f.write("%")
        f.write(f"{hard}")
        f.write("\n")
        f.write("///\n")
    return easy,medium,hard


bbb('math')
bbb("physics")
bbb("chemical")
bbb("biology")

#print(type(new_l))