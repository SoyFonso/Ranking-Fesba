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

'''
Gets the structure of the page  inputted
'''


def ranking_link(soup):
    return soup.find_all('a', {'class': 'morelink'})[-1]['href']

'''
Gets the link for the whole ranking (not a specified category)
'''


def gotocategory(soup, category):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition(f'">{category}')[0]
    return urljoin('https://www.badminton.es/ranking/', b.split('<th colspan="11"><a href="')[-1]).replace('amp;', '')

'''
Gets the link for the ranking of the specified category (referred as category), takes the data from the ranking page.
'''


def gotooviedo(soup):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('">Oviedo')[0]
    c = b.partition('Asturias')[2]
    return c.split('ogid')[1]

'''
Goes to the Oviedo team, now inside the specified category.
'''

def gotoplayer(soup, name):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition(f'">{name.upper()}')[0]
    return urljoin('https://www.badminton.es/ranking/', b.split('href="')[-1].replace('amp;', ''))

'''
Goes to the specified player specified as player.
'''


def getposition(soup): #TODO fix this thing
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition('IM Sub 19</a></td><td></td><td class="rank"><div style="">')[2]
    c = a.partition('PABLO SERRANO TASSIS</a></td><td class="rank"><div style="">')[2]
    return b.partition('</div>')[0], c.partition('</div>')[0]

'''
Gets the position of the player on each category where he/she participates.
'''


def getfinalrank():
    fesba_data = getdata(web_fesba)
    ranking = ranking_link(fesba_data)
    ranking_page = urljoin(web_fesba, ranking)
    ranking_page_data = getdata(ranking_page)
    category_link = gotocategory(ranking_page_data, categoria)
    specified_category_data = getdata(category_link)
    oviedo = category_link + '&ogid' + gotooviedo(specified_category_data)
    oviedo_data = getdata(oviedo)
    player = gotoplayer(oviedo_data, nombre)

    player_data = getdata(player)
    final_rank = f'IM 19: {getposition(player_data)[0]} \nDM 19 Pablo Serrano: {getposition(player_data)[1]}'
    messagebox.showinfo(message=final_rank, title=f"Ranking de {nombre}")



root = tkinter.Tk()
root.title("Ranking ESP Junior")

window_width = 480
window_height = 360

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


selectcategory = tkinter.Label(root, text='Selecciona categoria:')
selectcategory.place(x=240 , y=30)

botonsub19 = ttk.Button(root, text='Sub 19')
botonsub19.place(x=48, y=36)

botonsub17 = ttk.Button(root, text='Sub 17')
botonsub17.place(x=432, y=36)

botonsub15 = ttk.Button(root, text='Sub 15')
botonsub15.place(x=240, y=180)

botonsub13 = ttk.Button(root, text='Sub 13')
botonsub13.place(x=48, y=324)

botonsub11 = ttk.Button(root, text='Sub 11')
botonsub11.place(x=432, y=324)

root.mainloop()


