from db_manager import DBManager
from user import User
from werkzeug.security import check_password_hash

class LogUser(User):
    
    
    def __init__(self, username: str, password: str, db: object) -> None:
        
        self.__messages = []
        self.__db = db
        self.__redirection = None
        
        if self.test_username(username) and self.test_password(password):
            self.__username = username
            self.__password = password
            
            self.check_password_match()
            
            
    def test_username(self, username: str) -> bool:
        
        result = super().test_username(username, self.__messages)
        if not result:
            return False
        
        response = self.__db.search_for_username(username)
        if len(response) == 0:
            self.__messages.append('Este nome de usuário não existe!!!')
            return False
            
        return True
        
        
    def test_password(self, password: str) -> bool:
        return super().test_password(password, self.__messages)
    
    
    def is_all_okay(self) -> bool:
        return super().is_all_okay(
            self.__messages, 
            'Logado com sucesso!',
            self.set_redirection, 
            '/', 
            '/login')
        
    
    def set_redirection(self, route: str) -> None:
        
        self.__redirection = route
    
    
    def get_redirection(self) -> str:
        
        return self.__redirection
    
    
    def get_messages(self) -> list:
        
        return self.__messages
    
    
    def check_password_match(self) -> None:
        
        p_hash = self.__db.get_password_hash_from_user(self.__username)[0][0]
        
        print(self.__password)
        if not check_password_hash(p_hash, self.__password):
            self.__messages.append('Senha incorreta!!')
