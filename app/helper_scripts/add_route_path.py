''' Simple script responsible for getting the names of all 
locations,then formatting into a route like format and adding
it into the DB '''

import sqlite3 as sql

connection = sql.connect('../turitiba.db')
cursor = connection.cursor()

location_names = cursor.execute('SELECT name FROM locations').fetchall()

for name in location_names:
    
    route = name[0].replace(' ', '-').lower()
    cursor.execute('''UPDATE locations
                   SET route = ?
                   WHERE name = ?''',
                   (route, name[0],))
    connection.commit()
    
connection.close()