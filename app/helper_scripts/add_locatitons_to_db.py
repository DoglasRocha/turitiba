'''sqlite> .schema locations
CREATE TABLE locations (id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
address TEXT NOT NULL,
type TEXT NOT NULL,
description TEXT NOT NULL,
likes INTEGER NOT NULL, maps_link TEXT NOT NULL);


sqlite> .schema photos
CREATE TABLE photos (location_id INTEGER NOT NULL,
path TEXT NOT NULL,
FOREIGN KEY(location_id) REFERENCES locations(id));'''

import sqlite3 as sql
import wikipedia

'''locations = ['Jardim_Botânico_de_Curitiba', 'Parque_Barigui', 'Parque_Tanguá',
             'Parque_Tingui', 'Ópera_de_Arame', 'Bosque_do_Papa', 'Bosque_Alemão',
             'Memorial_Ucraniano', 'Museu_do_Expedicionário', 'Parque_da_Ciência_Newton_Freire_Maia',
             'Jardim_Zoológico_de_Curitiba', 'Rua_XV_de_Novembro_(Curitiba)',
             'Museu_Oscar_Niemeyer', 'Museu_Paranaense', 'Palacete_dos_Leões',
             'Paço_da_Liberdade', 'Museu_Egípcio_e_Rosa_Cruz', 'Parque_Bacacheri',
             'Passeio_Público_(Curitiba)', 'Museu_do_Holocausto_de_Curitiba']'''
             
locations = ['Rua XV de Novembro (Curitiba)', 'Passeio Público (Curitiba)']

connection = sql.connect('../turitiba.db')
cursor = connection.cursor()

for location in locations:
    
    wikipedia.set_lang('pt')
    page = wikipedia.page(location)
    title = page.title
    summary = page.summary
    likes = 0
    maps_link = f'https://www.google.com.br/maps/search/{location}'.replace(' ', '_')
    info = f'https://pt.wikipedia.org/wiki/{location}'.replace(' ', '_')
    images = page.images if len(page.images) > 0 else None

    cursor.execute('''INSERT INTO locations (name, description, likes, maps_link, info)
                VALUES (?, ?, ?, ?, ?)''',
                    (title,
                    summary,
                    0,
                    maps_link,
                    info))
    connection.commit()
    
    with open('images.txt', 'a') as f:
        f.write(f'{title}: {", ".join(images)}\n\n')
        
connection.close()

