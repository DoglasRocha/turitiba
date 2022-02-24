import sqlite3 as sql

class DBManager:
    
    
    def __init__(self, path_to_db: str) -> None:
        
        self.path_to_db = path_to_db
        
    
    def add_user_to_db(self, username: str, name: str, email: str, 
                       password_hash: str) -> None:
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        cursor.execute('''INSERT INTO users (username, name, email, password_hash)
                       VALUES (?, ?, ?, ?)''',
                       (username,
                       name,
                       email,
                       password_hash))
        connection.commit()
        
        connection.close()
        
        
    def get_all_usernames(self) -> list:
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        usernames = cursor.execute('''SELECT username FROM users''').fetchall()
        
        connection.commit()
        connection.close()
        
        return usernames
    
    
    def get_all_emails(self) -> list:
        
        connection = sql.connect(self.path_to_db)
        cursor = connection.cursor()
        
        emails = cursor.execute('''SELECT email FROM users''').fetchall()
        
        connection.commit()
        connection.close()
        
        return emails
        