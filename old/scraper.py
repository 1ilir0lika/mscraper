import requests
import re
from tabulate import tabulate
from bs4 import BeautifulSoup
import os

URL = "https://www.fersinaviaggi.it/crociere/c_msc_crociere/g_"
#link per testing
#URL = "https://www.fersinaviaggi.it/crociere/m_luglio_2023/c_msc_crociere/p_bari/d_6-9/g_"

all_rows = []
finlinks=[]
i = 1
while True:
    page = requests.get(URL + str(i))
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="elenco")
    names = results.find_all(class_="titolobr")
    if len(names) == 0:  # Controlla se l'elenco dei nomi è vuoto
        break
    links = results.find_all(class_="bottonevedi")
    days = results.find_all("span", id=re.compile("Repeater1_duratavedi_\d"))
    prices = results.find_all("div", id="vistaprezzi")
    rows = []
    for k in range(len(names)):
        row = []
        name = names[k].text
        day = days[k].text
        price = prices[k].text
        link=links[k].get("href")
        #esempio filtro
        if not (re.search("Southam|MEDITERRANEO|CARAIBI|MAR ROSSO", name) or re.search("[1-5]", day)) and re.search("BALCONE:\n[0-5]\d\d\,\d\d", price) :
        #filtro per testing
        #if True:
            row.append(name)
            row.append(day)
            row.append(price)
            #row.append(link)
            #pagina
            row.append(i)
            finlinks.append(link)
            rows.append(row)

    all_rows.extend(rows)
    #far incrementare prima per far funzionare link
    i += 1


print(tabulate(all_rows, headers=["destinazione", "notti", "prezzi","pagina"], showindex="always", tablefmt="heavy_grid"))
#far aprire link richiesto
while True:
    link = input("quale offerta vuoi aprire?\n")
    if int(link)<=len(finlinks):
        os.system("brave "+URL.replace("g_","")+finlinks[int(link)])
        break
    else: 
        print("\ninput troppo grande\n")
