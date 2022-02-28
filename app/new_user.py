from werkzeug.security import generate_password_hash
from user import User

class NewUser(User):
    
    
    def __init__(self, name: str, email: str, username: str, 
                 password: str, confirm_password: str, db: object) -> None:
        
        self.__messages = []
        self.__redirection = None
        self.__db = db
        
        if self.test_name(name):
            self.__name = name

        if self.test_email(email):
            self.__email = email
            
        if self.test_username(username):
            self.__username = username
            
        if self.test_password(password):
            self.__password = password
            
        if self.test_confirm_password(password, confirm_password):
            self.__confirm_password = confirm_password
        
    
    def test_name(self, name: str) -> bool:

        if not (len(name) > 0 and ' ' in name):
            
            self.__messages.append('Nome inválido!!!')
            return False
        
        return True
    
    def test_email(self, email: str) -> bool:
    
        test_value = []
    
        if not ('@' in email and '.' in email):
            
            self.__messages.append('E-mail inválido!!!')
            test_value.append(False)        
    
        all_emails = self.__db.get_all_emails()
        for mail in all_emails:
            
            if (email == mail[0]):
            
                self.__messages.append('Este email já foi cadastrado.')
                test_value.append(False)
                break
            
        return all(test_value)
    
    
    def test_username(self, username: str) -> bool:
        
        test_value = []
        
        result = super().test_username(
            username,
            self.__messages)
        test_value.append(result)
        
        all_usernames = self.__db.get_all_usernames()
        for user in all_usernames:
            
            if (username == user[0]):
                
                self.__messages.append('Este nome de usuário já foi escolhido!!!')
                test_value.append(False)
                
        return all(test_value)
    
    def test_password(self, password: str) -> bool:
        return super().test_password(password, self.__messages)
    

    def test_confirm_password(self, password: str, confirm_password: 
        str) -> bool:
    
        if not (password == confirm_password):
            
            self.__messages.append('As senhas digitadas não são iguais!!!')
            return False
        
        return True


    def get_messages(self) -> list:
        
        return self.__messages
    
    
    def is_all_okay(self) -> bool:
        
        return super().is_all_okay(
            self.__messages,
            'Cadastrado com sucesso!',
            self.set_redirection,
            '/login', 
            '/register'
        )
    
    
    def set_redirection(self, route: str) -> str:
        self.__redirection = route
    
    
    def get_redirection(self) -> str:
        return self.__redirection
    
    
    def send_to_db(self) -> None:
        self.__db.add_user_to_db(
            self.__username.lower(), self.__name, 
            self.__email.lower(), 
            generate_password_hash(self.__password)
        )

    