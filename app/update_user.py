from tabnanny import check
from db_manager import DBManager
from user import User
from werkzeug.security import check_password_hash, generate_password_hash


class UpdateUser(User):
    
    
    def __init__(self, name: str, email: str, username: str,
                 current_password: str, new_password: str,
                 confirm_password: str, db: DBManager) -> None:
        
        self.__db = db
        self.__username = username
        self.__current_data = self.__db.get_user_info(username)[0]
        self.__redirection = None
        self.__messages = []
        self.__new_data = {}
        self.__successful_message = 'Usuário atualizado!'
        
        if self.test_name(name):
            self.__new_data['name'] = name
            
        if self.test_email(email):
            self.__new_data['email'] = email
        
        if (current_password != ''
                and new_password != ''
                and confirm_password != ''):
            if (self.test_password(new_password)
                    and self.test_confirm_password(
                        new_password, confirm_password
                    )
                    and self.old_password_match(current_password)):
                self.__new_data['password_hash'] = generate_password_hash(
                    new_password
                )
                self.__successful_message = 'Usuário e senha atualizados!'        
    
    
    def test_name(self, name: str) -> bool:

        if not (len(name) > 0 and ' ' in name):
            
            self.__messages.append('Nome inválido!!!')
            return False
        
        if name == self.__current_data[0]:
            
            return False
        
        return True
    
    
    def test_email(self, email: str) -> bool:
    
        if not ('@' in email and '.' in email):
            
            self.__messages.append('E-mail inválido!!!')
            return False        
    
        result = self.__db.search_for_email(email)
        if (len(result) > 0):
            
            self.__messages.append('Este email já foi cadastrado.')
            return False

        if (email == self.__current_data[1]):
            return False
            
        return True
    
    
    def test_password(self, password: str) -> bool:
        return super().test_password(password, self.__messages)
    
    
    def test_confirm_password(self, password: str, 
                              confirm_password: str) -> bool:        
        if (password != confirm_password):
            
            self.__messages.append('A confirmação da senha não bate com a nova senha!!!')
            return False
        
        return True
    
    
    def old_password_match(self, old_password: str) -> bool:
        
        old_password_hash = self.__db.get_password_hash_from_user(
            self.__username)[0][0]
        
        if not check_password_hash(old_password_hash, old_password):
            
            self.__messages.append('A senha antiga não confere!!!')
            return False
        
        return True
    
    
    def test_username(self) -> bool:
        pass
    
    
    def is_all_okay(self) -> bool:
        return super().is_all_okay(
            self.__messages, self.__successful_message, 
            self.set_redirection, '/', f'/user/{self.__username}')
    
    
    def get_messages(self) -> list:
        return self.__messages
    
    
    def set_redirection(self, route: str) -> None:
        self.__redirection = route
    
    
    def get_redirection(self) -> str:
        return self.__redirection
    
    
    def update_user_in_db(self) -> str:
        
        self.__db.update_user(self.__new_data, self.__username)