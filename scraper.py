import requests
import re
from tabulate import tabulate
from bs4 import BeautifulSoup
import datetime

date = datetime.date.today()
URL = "https://www.fersinaviaggi.it/crociere/z_nord_europa/c_msc_crociere/g_"
all_rows = []

i = 1
while True:
    page = requests.get(URL + str(i))
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="elenco")
    names = results.find_all(class_='titolobr')

    if len(names) == 0:  # Controlla se l'elenco dei nomi è vuoto
        break

    days = results.find_all("span", id=re.compile("Repeater1_duratavedi_\d"))
    prices = results.find_all("div", id="vistaprezzi")

    rows = []
    for k in range(len(names)):
        row = []
        name = names[k].text
        day = days[k].text
        price = prices[k].text
        if not (re.search("Southam", name) or re.search("[1-5]", day) or re.search("BALCONE:\nn.d.", price)):
            row.append(name)
            row.append(day)
            row.append(price)
            rows.append(row)

    all_rows.extend(rows)
    i += 1

file = open('data/' + str(date) + '.pr', "w")
file.write(str(all_rows))
file.write("\n" + str(date))
file.close()

print(tabulate(all_rows, headers=["destinazione", "notti", "prezzi"], showindex="always", tablefmt="heavy_grid"))
