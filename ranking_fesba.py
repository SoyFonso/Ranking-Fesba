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


def gotocategory(soup, string):
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition(f'">{string}')[0]
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


def getposition(soup):  # TODO fix this thing
    nombrepareja = 'PABLO SERRANO TASSIS'
    categoria = f'{modalidad[0]} {category[0]}'
    a = str(soup.find_all('table', {'class': 'ruler'}))
    b = a.partition(f'{categoria}</a></td><td></td><td class="rank"><div style="">')[2]
    c = a.partition(f'{nombrepareja}</a></td><td class="rank"><div style="">')[2]
    return b.partition('</div>')[0], c.partition('</div>')[0]


'''
Gets the position of the player on each category where he/she participates.
'''


def getfinalrank():
    fesba_data = getdata(web_fesba)
    ranking = ranking_link(fesba_data)
    ranking_page = urljoin(web_fesba, ranking)
    ranking_page_data = getdata(ranking_page)
    categoria = f'{modalidad[0]} {category[0]}'
    category_link = gotocategory(ranking_page_data, categoria)
    specified_category_data = getdata(category_link)
    oviedo = category_link + '&ogid' + gotooviedo(specified_category_data)
    oviedo_data = getdata(oviedo)
    player = gotoplayer(oviedo_data, nombre[0])
    player_data = getdata(player)
    final_position = getposition(player_data)
    return final_position


def gettocategory(label, combobox, button):
    label.place(x=window_width / 2, y=window_height / 2 - 40, anchor='center', relheight=0.1)
    combobox.place(x=window_width / 2, y=window_height / 2, anchor='center', relheight=0.1)
    button.place(x=window_width/2, y=window_height/2 + 50, anchor='center')


def gettotrial(boton, combobox, label, combobox1, label1, boton1, boton2, lista):
    lista.clear()
    categoriaa = combobox.get()
    if categoriaa != '':
        lista.append(categoriaa)
        boton.place_forget()
        combobox.place_forget()
        label.place_forget()
        combobox1.place(x=window_width/2, y=window_height/2, anchor='center', relheight=0.1)
        label1.place(x=window_width/2, y=window_height/2 - 40, anchor='center', relheight=0.1)
        boton1.place(x=window_width / 2 + 100, y=window_height / 2 + 100, anchor='center')
        boton2.place(x=window_width/2, y=window_height/2 + 50, anchor='center')

    else:
        messagebox.showinfo(title='Error', message='Debes seleccionar una categoría.')


def gobackcategory(combobox, boton, label, boton1, label1, combobox1):
    boton.place(x=window_width/2, y=window_height/2 + 50, anchor='center')
    combobox.place(x=window_width/2, y=window_height/2, anchor='center', relheight=0.1)
    label.place(x=window_width / 2, y=window_height / 2 - 40, anchor='center', relheight=0.1)
    boton1.place_forget()
    label1.place_forget()
    combobox1.place_forget()


def gettoplayers(boton, combobox, label, combobox1, label1, boton1, boton2, boton3, lista):
    lista.clear()
    modalidadd = combobox.get()
    if modalidadd != '':
        lista.append(modalidadd)
        boton.place_forget()
        combobox.place_forget()
        label.place_forget()
        boton2.place_forget()
        combobox1.place(x=window_width/2, y=window_height/2, anchor='center', relheight=0.1)
        label1.place(x=window_width/2, y=window_height/2 - 40, anchor='center', relheight=0.1)
        boton1.place(x=window_width/2, y=window_height/2 + 50, anchor='center')
        boton3.place(x=window_width / 2 + 100, y=window_height / 2 + 100, anchor='center')
        categoria = f'{modalidad[0]} {category[0]}'
        for k, v in dictnombres.items():
            if k == categoria:
                uwu = v.copy()
                listadenombres.extend(uwu)
                print(listadenombres)
        combobox1['value'] = listadenombres

    else:
        messagebox.showinfo(title='Error', message='Debes seleccionar una modalidad.')


def gobackplayers(boton, combobox, label, boton1, combobox1, label1, boton2, boton3):
    boton.place(x=window_width / 2, y=window_height / 2 + 50, anchor='center')
    combobox.place(x=window_width / 2, y=window_height / 2, anchor='center', relheight=0.1)
    label.place(x=window_width / 2, y=window_height / 2 - 40, anchor='center', relheight=0.1)
    boton3.place(x=window_width / 2 + 100, y=window_height / 2 + 100, anchor='center')
    boton1.place_forget()
    combobox1.place_forget()
    label1.place_forget()
    boton2.place_forget()


def getranking(boton, combobox, label, boton1, label1, combobox1, boton2, lista):
    lista.clear()
    nombree = combobox.get()
    if nombree != '':
        lista.append(nombree)
        boton.place_forget()
        combobox.place_forget()
        label.place_forget()
        boton1.place_forget()
        messagebox.showinfo(title=f'Ranking de {nombree}', message=f'{getfinalrank()}')
        gettocategory(label1, combobox1, boton2)

    else:
        messagebox.showinfo(title='Error', message='Debes seleccionar un jugador.')


category = []

modalidad = []

nombre = []

listadenombres = []

dictnombres = {
    'IM Sub 19': ['ADRIAN ALVAREZ GONZALEZ', 'MARCOS GARCIA MARTINEZ', 'ALFONSO PINTO GARCIA',
                  'JESUS DE BURGOS MAZAIRA', 'ALEJANDRO LOPEZ ALVAREZ', 'Adolfo López González'],

    'IF Sub 19': ['LAURA ALVAREZ GONZALEZ', 'JANA VILLANUEVA AGENJO', 'LEYRE SUBERVIOLA USTARROZ',
                  'AINARA FERNÁNDEZ SUCO', 'VIOLETA MIGOYA GIL', 'RAQUEL SOTO MARTÍNEZ', 'IRENE FERNANDEZ FERNANDEZ',
                  'LAURA GARIJO GOMEZ', 'IRIA JUNCAL PINTO GARCIA', 'OLAYA GARCIA FERNANDEZ'],

    'DM Sub 19': ['JESUS DE BURGOS MAZAIRA', 'ALFONSO PINTO', 'MARCOS GARCIA MARTINEZ'],
    'DF Sub 19': ['OLAYA GARCIA FERNANDEZ', 'JANA VILLANUEVA AGENJO', 'AINARA FERNANDEZ SUCO', 'VIOLETA MIGOYA GIL',
                  'IRENE FERNADEZ FERNANDEZ', 'NATALIA LAMARCA GARCÍA', 'RAQUEL SOTO MARTÍNEZ'],

    'DX Sub 19': ['Adolfo López González', 'OLAYA GARCIA FERNANDEZ', 'ALEJANDRO LOPEZ ALVAREZ',
                  'LEYRE SUBERVIOLA USTARROZ', 'JESUS DE BURGOS MAZAIRA', 'NATALIA LAMARCA GARCÍA'],
    'IM Sub 17': ['ALEJANDRO LOPEZ ALVAREZ', 'JESUS DE BURGOS MAZAIRA', 'Adolfo López González', 'Yago García Fernandez'],
    'IF Sub 17': ['VIOLETA MIGOYA GIL', 'IRENE FERNANDEZ FERNANDEZ', 'LAURA GARIJO GOMEZ', 'MIREYA PEREZ CANO'],
    'DM Sub 17': ['JESUS DE BURGOS MAZAIRA', 'Adolfo López González'],
    'DF Sub 17': []
}

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

selectmodalidad = tkinter.Label(root, text='Selecciona modalidad:')

selectplayer = tkinter.Label(root, text='Selecciona un jugador:')

categorialist = ttk.Combobox(root, values=['Sub 19', 'Sub 17', 'Sub 15', 'Sub 13', 'Sub 11'], state='readonly')

modalidadlist = ttk.Combobox(root, value=['IM', 'IF', 'DM', 'DF', 'DX'], state='readonly')

playerlist = ttk.Combobox(root, value=[listadenombres], state='readonly')


botoncategoria = ttk.Button(root, text='Siguiente', command=lambda: gettotrial(botoncategoria, categorialist, selectcategory, modalidadlist, selectmodalidad, botonvolvercategoria, botonmodalidad, category))

botonmodalidad = ttk.Button(root, text='Siguiente', command=lambda: gettoplayers(botonmodalidad, modalidadlist, selectmodalidad, playerlist, selectplayer, botonjugador, botonvolvercategoria, botonvolvermodalidad, modalidad))

botonvolvercategoria = ttk.Button(root, text='Volver', command=lambda: gobackcategory(categorialist, botoncategoria, selectcategory, botonvolvercategoria, selectmodalidad, modalidadlist))

botonjugador = ttk.Button(root, text='Siguiente', command=lambda: getranking(botonjugador, playerlist, selectplayer, botonvolvermodalidad, selectcategory, categorialist, botoncategoria, nombre))

botonvolvermodalidad = ttk.Button(root, text='Volver', command=lambda: gobackplayers(botonmodalidad, modalidadlist, selectmodalidad, botonvolvermodalidad, playerlist, selectplayer, botonjugador, botonvolvercategoria))

gettocategory(selectcategory, categorialist, botoncategoria)

root.mainloop()
