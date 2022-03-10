import sqlite3 as sql

class DBManager:
    '''
    Class that deals with all the SQL instructions. All the methods
    that require any SQL query are written in this class.
    When instantiated, receives the path to the Database.
    '''
    
    def __init__(self, path_to_db: str) -> None:
        
        self.path_to_db = path_to_db
    
    
    def create_connection(self) -> None:
        '''
        Creates the connection with the database and the cursor,
        to avoid repetitive instructions.
        
        Returns the connection and the cursor.
        '''
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        return connection, cursor
        
    
    def close_connection(self, connection: object) -> None:
        
        connection.commit()
        connection.close()
    
    
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
        
        self.close_connection(connection)
    
    
    def search_for_email(self, email: str) -> list:
        
        connection, cursor = self.create_connection()
        
        emails = cursor.execute('''SELECT email 
                                FROM users
                                WHERE email = ?''',
                                (email,)).fetchone()
        
        self.close_connection(connection)
        
        return emails
        
        
    def search_for_username(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        result = cursor.execute(
            '''SELECT username
            FROM users
            WHERE username = ?''',
            (username,)).fetchone()
        
        self.close_connection(connection)
        
        return result


    def get_password_hash_from_user(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        p_hash = cursor.execute('''SELECT password_hash
                                FROM users
                                WHERE username = ?''',
                                (username,)).fetchone()
        
        self.close_connection(connection)
        
        return p_hash
    
    
    def get_user_info(self, username: str) -> list:
        
        connection, cursor = self.create_connection()
        
        user_info = cursor.execute('''SELECT name, email
                                   FROM users
                                   WHERE username = ?''',
                                   (username,)).fetchone()
        
        self.close_connection(connection)
        return user_info
    
    
    def get_user_info_to_comments(self, user_id: int) -> tuple:
        
        connection, cursor = self.create_connection()
        
        user_info = cursor.execute('''SELECT name, username
                                   FROM users
                                   WHERE id = ?''',
                                   (user_id,)).fetchone()
        
        self.close_connection(connection)
        return user_info
    
    
    def update_user(self, new_data: dict, username: str) -> None:
        
        connection, cursor = self.create_connection()
        
        for key, value in new_data.items():
            
            cursor.execute(f'''UPDATE users
                           SET {key} = ?
                           WHERE username = ?''',
                           (value, username))
            self.connection.commit()
            
        self.close_connection(connection)
        
        
    def get_locations_samples(self) -> None:
        
        connection, cursor = self.create_connection()
        
        all_info = cursor.execute('''SELECT name, path, route
                                  FROM locations
                                  JOIN photos ON
                                  photos.location_id = locations.id
                                  ORDER BY likes DESC'''
                                  ).fetchall()
        
        self.close_connection(connection)
        
        return all_info
    
    
    def get_location_data(self, location_name: str) -> tuple:
        
        connection, cursor = self.create_connection()
        
        location_id = cursor.execute('''SELECT id
                                     FROM locations
                                     WHERE route = ?
                                     ''',
                                     (location_name,)).fetchone()

        location_info = cursor.execute('''SELECT name, description, likes, maps_link, info, route
                                       FROM locations
                                       WHERE id = ?''',
                                       location_id).fetchone()
        
        location_photos = cursor.execute('''SELECT path
                                        FROM photos
                                        WHERE location_id = ?''',
                                        location_id).fetchall()
        
        self.close_connection(connection)
        
        return location_info, location_photos
    
    
    def get_user_id(self, username: str) -> tuple:
        
        connection, cursor = self.create_connection()
        
        id_ = cursor.execute('''SELECT id
                             FROM users
                             WHERE username = ?''',
                             (username,)).fetchone()
        
        self.close_connection(connection)
        return id_
    
    
    def get_location_id(self, location_route: str) -> tuple:
        
        connection, cursor = self.create_connection()
        
        id_ = cursor.execute('''SELECT id
                             FROM locations
                             WHERE route = ?''',
                             (location_route,)).fetchone()
        
        self.close_connection(connection)
        return id_
    
    
    def search_for_like_in_location(self, user_id: int, 
                                    location_id: int) -> tuple:
        
        connection, cursor = self.create_connection()
        
        result = cursor.execute('''SELECT is_liking
                                FROM likes
                                WHERE user_id = ?
                                AND location_id = ?''',
                                (user_id, location_id)).fetchone()
        
        self.close_connection(connection)
        
        return result
    
    
    def unlike_location(self, user_id: int, 
                                location_id: int) -> None:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''UPDATE likes
                       SET is_liking = ?
                       WHERE location_id = ?
                       AND user_id = ?''',
                       (0, location_id, user_id,))
        connection.commit()
        
        self.close_connection(connection)
        
        
    def like_location(self, user_id: int,
                      location_id: int) -> None:
        
        connection, cursor = self.create_connection()
        cursor.execute('''UPDATE likes
                       SET is_liking = ?
                       WHERE user_id = ?
                       AND location_id = ?''',
                       (1, user_id, location_id))
        connection.commit()
        
        self.close_connection(connection)
        
    def insert_like_in_location(self, user_id: int,
                                location_id: int) -> None:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''INSERT INTO likes(user_id, location_id, is_liking)
                            VALUES (?, ?, 1)''',
                            (user_id, location_id))
        
        self.close_connection(connection)
        
        
    def get_likes_in_location(self, location_id: int) -> tuple:
        
        connection, cursor = self.create_connection()
        
        likes_count = cursor.execute('''SELECT COUNT(user_id)
                                        FROM likes
                                        WHERE location_id = ?
                                        AND is_liking = 1''',
                                        (location_id,)).fetchone()
        
        self.close_connection(connection)
        
        return likes_count
    
    
    def update_likes_in_location(self, location_id: int,
                                 likes_count: int) -> tuple:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''UPDATE locations
                            SET likes = ?
                            WHERE id = ?''',
                            (likes_count, location_id))
        
        self.close_connection(connection)
        
        
    def get_all_locations_id(self) -> list:
        
        connection, cursor = self.create_connection()
        
        result = cursor.execute('''SELECT id 
                                FROM locations''').fetchall()
        
        self.close_connection(connection)
        return result
    
    
    def insert_comment_in_location(self, comment: str, user_id: int, 
                                   location_id: int, date) -> None:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''INSERT INTO comments
                       VALUES (?, ?, ?, ?)''',
                       (comment, 
                        user_id, 
                        location_id, 
                        date))
        
        connection.commit()
        
        self.close_connection(connection)
        
        
    def get_comments_from_location(self, location_id: int) -> list:
        
        connection, cursor = self.create_connection()
        
        comments = cursor.execute('''SELECT *
                                  FROM comments
                                  WHERE location_id = ?
                                  ORDER BY date DESC''',
                                  (location_id,)).fetchall()
        
        self.close_connection(connection)
        return comments
    
    
    def delete_comment(self, user_id: int, location_id: int,
                       comment: str) -> None:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''DELETE FROM comments
                       WHERE user_id = ? 
                       AND location_id = ?
                       AND comment = ?''',
                       (user_id, location_id, comment))
        connection.commit()
        
        connection.close()
        
        
    def search_for_location(self, query: str) -> list:
        
        connection, cursor = self.create_connection()
        
        all_info = cursor.execute('''SELECT name, path, route, description
                                  FROM locations
                                  JOIN photos ON
                                  photos.location_id = locations.id
                                  WHERE name LIKE ?
                                  ORDER BY path DESC''',
                                  (f'%{query}%',)).fetchall()
        
        self.close_connection(connection)
        
        return all_info
    
    
    def search_location_names(self, search) -> list:
        
        connection, cursor = self.create_connection()
        
        result = cursor.execute('''SELECT name
                                FROM locations
                                WHERE name LIKE ?''', 
                                (f'%{search}%',)).fetchall()
        
        self.close_connection(connection)
        
        return result