import tkinter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tkinter import messagebox, ttk

web_fesba = 'https://www.badminton.es/'


def getdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def ranking_link(soup):
    return soup.find_all('a', {'class': 'morelink'})[-1]['href']


def gotoim19(soup):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('href="')[2]
    return urljoin('https://www.badminton.es/ranking/', b.partition('">')[0]).replace('amp;', '')


def gotoif19(soup):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('href="')[2]
    c = b.partition('">IF Sub 19')[0]
    return urljoin('https://www.badminton.es/ranking/', c.partition('<th colspan="11"><a href="')[2]).replace('amp;', '')


def gotooviedo(soup):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('">Oviedo')[0]
    c = b.partition('Asturias')[2]
    return c.split('ogid')[1]


def gotoplayer(soup, name):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition(f'">{name.upper()}')[0]
    return urljoin('https://www.badminton.es/ranking/', b.split('href="')[-1].replace('amp;', ''))


def getposition(soup):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('IM Sub 19</a></td><td></td><td class="rank"><div style="">')[2]
    c = a.partition('PABLO SERRANO TASSIS</a></td><td class="rank"><div style="">')[2]
    return b.partition('</div>')[0], c.partition('</div>')[0]


def getfinalrankim():
    fesba_data = getdata(web_fesba)
    ranking = ranking_link(fesba_data)
    ranking_page = urljoin(web_fesba, ranking)
    ranking_page_data = getdata(ranking_page)
    im19 = gotoim19(ranking_page_data)
    im19_data = getdata(im19)
    oviedo = im19 + '&ogid' + gotooviedo(im19_data)
    oviedo_data = getdata(oviedo)
    player = gotoplayer(oviedo_data, nombre)
    print(player)
    player_data = getdata(player)
    final_rank = f'IM 19: {getposition(player_data)[0]} \nDM 19 Pablo Serrano: {getposition(player_data)[1]}'
    messagebox.showinfo(message=final_rank, title=f"Ranking de {nombre}")


def getfinalrankif():
    fesba_data = getdata(web_fesba)
    ranking = ranking_link(fesba_data)
    ranking_page = urljoin(web_fesba, ranking)
    ranking_page_data = getdata(ranking_page)
    if19 = gotoif19(ranking_page_data)
    if19_data = getdata(if19)
    oviedo = if19 + '&ogid' + gotooviedo(if19_data)
    oviedo_data = getdata(oviedo)


root = tkinter.Tk()
root.config(width=300, height=200)
root.title("Ranking ESP Junior")
label = tkinter.Label(root, text='Selecciona jugador:')
label.place(relx=0.5, rely=0.05, anchor='center')
nombre = 'Alfonso Pinto'
botonalfonso = ttk.Button(root, text=nombre, command=getfinalrankim)
botonalfonso.place(x=50, y=50)
root.mainloop()
