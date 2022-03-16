''' Script responsible for adding the images path
into the DB. Firstly, defines a function that returns
the formatted string of the image path. Then, defines
a list of dicts with the id, the name and the amount of images
- 1 (implementation detail, the main image of a locations
has to have the 999 index, the rest will be counted from 0.
So, because there is always a 999 index, amount - 1). 
Then, iterates over the list and adds all the images of a 
determined location '''


import sqlite3 as sql

def get_path(name: str, number: int) -> str:
    
    return f'./static/img/{name}-{number}.jpg'

'''1|Jardim Botânico de Curitiba
2|Parque Barigui
3|Parque Tanguá
4|Parque Tingui
5|Ópera de Arame
6|Bosque do Papa
7|Bosque Alemão
8|Memorial Ucraniano
9|Museu do Expedicionário
10|Parque da Ciência Newton Freire Maia
11|Jardim Zoológico de Curitiba
13|Museu Oscar Niemeyer
14|Museu Paranaense
15|Palacete dos Leões
16|Paço da Liberdade
17|Museu Egípcio e Rosa Cruz
18|Parque Bacacheri
20|Museu do Holocausto de Curitiba
21|Rua XV de Novembro (Curitiba)
22|Passeio Público (Curitiba)'''

locations = [
    {
        'id': 1,
        'name': 'botanico',
        'range': 3
    },
    {
        'id': 2,
        'name': 'barigui',
        'range': 4
    },
    {
        'id': 3,
        'name': 'tangua',
        'range': 2
    },
    {
        'id': 4,
        'name': 'tingui',
        'range': 1
    },
    {
        'id': 5,
        'name': 'opera-de-arame',
        'range': 2
    },
    {
        'id': 6,
        'name': 'bosque-do-papa',
        'range': 4
    },
    {
        'id': 7,
        'name': 'bosque-alemao',
        'range': 2
    },
    {
        'id': 8,
        'name': 'memorial-ucraniano',
        'range': 1
    },
    {
        'id': 9,
        'name': 'museu-expedicionario',
        'range': 5
    },
    {
        'id': 10,
        'name': 'parque-ciencia',
        'range': 0
    },
    {
        'id': 11,
        'name': 'zoologico',
        'range': 2
    },
    {
        'id': 13,
        'name': 'mon',
        'range': 0
    },
    {
        'id': 14,
        'name': 'paranaense',
        'range': 0
    },
    {
        'id': 15,
        'name': 'palacete-leoes',
        'range': 1
    },
    {
        'id': 16,
        'name': 'paco-liberdade',
        'range': 0
    },
    {
        'id': 17,
        'name': 'museu-egipcio',
        'range': 0
    },
    {
        'id': 18,
        'name': 'bacacheri',
        'range': 0
    },
    {
        'id': 20,
        'name': 'museu-holocausto',
        'range': 1
    },
    {
        'id': 21,
        'name': 'rua-xv',
        'range': 2
    },
    {
        'id': 22,
        'name': 'passeio-publico',
        'range': 1
    },
]

connection = sql.connect('../turitiba.db')
cursor = connection.cursor()

for location in locations:
    
    name = location['name']
    id_ = location['id']
    range_ = location['range']
    
    path = get_path(name, 999)
    
    cursor.execute('''INSERT INTO photos
                   VALUES (?, ?)''',
                   (id_, path))
    connection.commit()
    
    if range_ > 0:
        
        for i in range(1, range_ + 1):
            path = get_path(name, i)
            
            cursor.execute('''INSERT INTO photos
                   VALUES (?, ?)''',
                   (id_, path))
            connection.commit()
            