from abc import ABCMeta, abstractmethod

class User(metaclass=ABCMeta):
    
    
    @abstractmethod
    def test_username(self, username: str, messages: list) -> bool:
        
        
        if not (len(username) > 0 and ' ' not in username):
            
            messages.append('Nome de usuário inválido!!!')
            return False
        
        return True
    
    
    @abstractmethod
    def test_password(self, password: str, messages: list) -> bool:
    
        if not (len(password) >= 8):
            
            messages.append('Senha inválida!!!')
            return False
        
        return True
    
    
    @abstractmethod
    def is_all_okay(self, 
                    messages: list, 
                    message: str,
                    redirection_method: str,
                    successfull_route: str,
                    unsuccessfull_route: str) -> bool:
        
        if (len(messages) == 0):
            
            messages.append(message)
            redirection_method(successfull_route)
            return True
        
        redirection_method(unsuccessfull_route)
        return False
    
    
    @abstractmethod
    def get_redirection(self) -> str:
        pass
    
    
    @abstractmethod
    def get_messages(self) -> list:
        pass
    
    
    @abstractmethod
    def set_redirection(self, route: str) -> str:
        pass