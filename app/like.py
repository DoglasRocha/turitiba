from db_manager import DBManager
from reader import Reader

class Like:
    
    
    def __init__(self, db: DBManager, user_id: int, location_id: int,
                 username: str, location_route: str):
        
        self.__db = db
        self.__user_id = user_id
        self.__location_id = location_id
        self.__username = username
        self.__location_route = location_route
        self.__action = None
        self.__possible_actions = {
            'NEW_LIKE': self.insert_like,
            'UNLIKE': self.unlike,
            'LIKE_AGAIN': self.like_again
        }
        
        
    def set_action(self) -> None:
        
        user_has_register_in_likes_table = (
            Reader.user_has_register_in_likes_table(
                self.__db, self.__username, self.__location_route
            )
        )
        
        if not (user_has_register_in_likes_table):
            
            self.__action = 'NEW_LIKE'
            return self
        
        user_has_already_liked = Reader.user_has_liked(
            self.__db, self.__username, self.__location_route
        )
        
        if (user_has_already_liked):
            
            self.__action = 'UNLIKE'
            return self
        
        self.__action = 'LIKE_AGAIN'
        return self
    
    
    def action(self) -> None:
        
        action = self.__possible_actions[self.__action]
        action()
        self.update_likes()
    
    
    def insert_like(self) -> None:
        
        self.__db.insert_like_in_location(
            self.__user_id, self.__location_id
        )
    
    
    def unlike(self) -> None:
        
        self.__db.unlike_location(
            self.__user_id, self.__location_id
        )
    
    
    def like_again(self) -> None:
        
        self.__db.like_location(
            self.__user_id, self.__location_id
        )
        
        
    def update_likes(self) -> None:
        
        likes_count = Reader.get_likes_in_location(self.__db, 
                                                   self.__location_id)
    
        self.__db.update_likes_in_location(self.__location_id, 
                                           likes_count)