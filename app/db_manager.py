import sqlite3 as sql

class DBManager:
    '''
    Class that deals with all the SQL instructions. All the methods
    that require any SQL query are written in this class.
    When instantiated, receives the path to the Database.
    '''
    
    def __init__(self, path_to_db: str) -> None:
        
        self.path_to_db = path_to_db
        
    
    def create_connection(self) -> tuple:
        '''
        Creates the connection with the database and the cursor,
        to avoid repetitive instructions.
        
        Returns the connection and the cursor.
        '''
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        return connection, cursor
        
    
    def add_user_to_db(self, username: str, name: str, email: str, 
                       password_hash: str) -> None:
        '''Adds a user to the DB. 
        
        Receives the username, name, email and password hash and inserts
        them to the DB.
        
        Then closes the connection.'''
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''INSERT INTO users (username, name, email, password_hash)
                       VALUES (?, ?, ?, ?)''',
                       (username,
                       name,
                       email,
                       password_hash))
        connection.commit()
        
        connection.close()
    
    
    def search_for_email(self, email: str) -> list:
        
        connection, cursor = self.create_connection()
        
        emails = cursor.execute('''SELECT email 
                                FROM users
                                WHERE email = ?''',
                                (email,)).fetchall()
        
        connection.commit()
        connection.close()
        
        return emails
        
        
    def search_for_username(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        result = cursor.execute(
            '''SELECT username
            FROM users
            WHERE username = ?''',
            (username,)).fetchall()
        
        connection.commit()
        connection.close()
        
        return result


    def get_password_hash_from_user(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        p_hash = cursor.execute('''SELECT password_hash
                                FROM users
                                WHERE username = ?''',
                                (username,)).fetchall()
        
        connection.commit()
        connection.close()
        
        return p_hash
    
    
    def get_user_info(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        user_info = cursor.execute('''SELECT name, email
                                   FROM users
                                   WHERE username = ?''',
                                   (username,)).fetchall()
        
        connection.commit()
        connection.close()
        
        return user_info
    
    
    def update_user(self, new_data: dict, username: str) -> None:
        
        connection, cursor = self.create_connection()
        
        for key, value in new_data.items():
            
            cursor.execute(f'''UPDATE users
                           SET {key} = ?
                           WHERE username = ?''',
                           (value, username))
            connection.commit()
            
        connection.close()
        
        
    def get_locations_samples(self) -> None:
        
        connection, cursor = self.create_connection()
        
        all_info = cursor.execute('''SELECT name, path
                                  FROM locations
                                  JOIN photos ON
                                  photos.location_id = locations.id
                                  ORDER BY path DESC'''
                                  ).fetchall()
        
        connection.commit()
        connection.close()
        
        return all_info
        
        