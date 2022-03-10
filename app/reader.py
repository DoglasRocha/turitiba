from db_manager import DBManager

class Reader:
    
    @staticmethod
    def get_user_id(db: DBManager, username: str) -> int:
        
        return db.get_user_id(username)[0]
    
    
    @staticmethod
    def get_location_id(db: DBManager, location_route: str) -> int:
        
        return db.get_location_id(location_route)[0]
    
    
    @staticmethod
    def get_user_info(db: DBManager, username: str) -> dict:
        
        name, email = db.get_user_info(username)
        info = {
            'username': username,
            'name': name,
            'email': email
        }
        
        return info
    
    
    @staticmethod
    def get_sample_locations_sample(db: DBManager, 
                                    size_of_the_sample: int) -> list:
        
        raw_sample = db.get_locations_samples()
        names = []
        paths = []
        routes = []
        
        for name, path, route in raw_sample:
            if name not in names:
                names.append(name)
                paths.append(path)
                routes.append(route)
                
        treated_sample = []
        for name, path, route in zip(names, paths, routes):
            treated_sample.append({
                'name': name,
                'path': path,
                'route': route
            })
            
        return treated_sample[:size_of_the_sample]
    
    
    @staticmethod
    def get_location_data(db: DBManager, location_route: str) -> dict:
        
        raw_data, photos = db.get_location_data(location_route)
    
        name, description, likes, maps_link, info, route = raw_data
    
        treated_photos = []
        for photo in photos:
            treated_photos.append('.' + photo[0])
            
        data = {
            'name': name,
            'description': description,
            'likes': likes,
            'maps_link': maps_link,
            'info': info,
            'route': route,
            'photos': treated_photos
        }
        
        return data
    
    
    @staticmethod
    def user_has_register_in_likes_table(
        db: DBManager, username: str, location_route: str
    ) -> bool:
        
        user_id = Reader.get_user_id(db, username)
        location_id = Reader.get_location_id(db, location_route)
        
        user_has_register = db.search_for_like_in_location(
            user_id, location_id
        )
        
        return user_has_register
    
    
    @staticmethod
    def user_has_liked(db: DBManager, username: str, 
                       location_route: str) -> bool:
        
        has_register_in_likes_table = (
            Reader.user_has_register_in_likes_table(
                db, username, location_route
            )
        )
        
        if not (has_register_in_likes_table):
            return False
        
        return bool(has_register_in_likes_table[0])


    @staticmethod
    def get_likes_in_location(db: DBManager, location_id: int) -> int:
        
        likes = db.get_likes_in_location(location_id)[0]
        
        return likes