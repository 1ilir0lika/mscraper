import requests
import re
from tabulate import tabulate
from bs4 import BeautifulSoup
import datetime

URL = "https://www.fersinaviaggi.it/crociere/z_nord_europa/m_agosto_2023/c_msc_crociere"
page = requests.get(URL)

date = datetime.date.today()

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="elenco")

names = results.find_all(class_='titolobr')
days = results.find_all("span", id=re.compile("Repeater1_duratavedi_\d"))
prices = results.find_all("div", id="vistaprezzi")

rows = []
for k in range(0, len(names)):
    row = []
    name = names[k].text
    day = days[k].text
    price = prices[k].text
    #escludi inghilterra(fare il passaporto richiede anni) e crociere <= 5 giorni e crociere senza camera con balcone
    if not (re.search("Southam",name) or re.search("[1-5]",day) or re.search("BALCONE:\nn.d.",price)):
        row.append(name)
        row.append(day)
        row.append(price)
        rows.append(row)

print(tabulate(rows, headers=["destinazione", "notti", "prezzi"], showindex="always", tablefmt="heavy_grid"))
