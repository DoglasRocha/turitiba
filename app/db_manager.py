import sqlite3 as sql

class DBManager:
    
    
    def __init__(self, path_to_db: str) -> None:
        
        self.path_to_db = path_to_db
        
    
    def create_connection(self) -> tuple:
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        return connection, cursor
        
    
    def add_user_to_db(self, username: str, name: str, email: str, 
                       password_hash: str) -> None:
        
        connection, cursor = self.create_connection()
        
        cursor.execute('''INSERT INTO users (username, name, email, password_hash)
                       VALUES (?, ?, ?, ?)''',
                       (username,
                       name,
                       email,
                       password_hash))
        connection.commit()
        
        connection.close()
        
        
    def get_all_usernames(self) -> list:
        
        connection, cursor = self.create_connection()
        
        usernames = cursor.execute('''SELECT username FROM users''').fetchall()
        connection.commit()
        connection.close()
        
        return usernames
    
    
    def get_all_emails(self) -> list:
        
        connection, cursor = self.create_connection()
        
        emails = cursor.execute('''SELECT email FROM users''').fetchall()
        
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