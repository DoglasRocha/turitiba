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
    def get_locations_sample(db: DBManager, 
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
    
    
    @staticmethod
    def get_comments_from_location(db: DBManager, 
                                   location_route: str) -> list:
        
        location_id = Reader.get_location_id(db, location_route)
        raw_data = db.get_comments_from_location(location_id)
        
        treated_data = []
        for data in raw_data:
            
            comment, user_id, location_id, date = data
            formatted_date = Reader.format_date(date)
            Reader.format_date(date)
            name, username = db.get_user_info_to_comments(user_id)
            treated_data.append({
                'comment': comment,
                'date': formatted_date,
                'name': name,
                'username': username,
                'user_id': user_id, 
                'location_id': location_id
            })
            
        return treated_data
    
    
    @staticmethod
    def format_date(date: str):
        
        year, month, day = tuple(date.split(' ')[0].split('-'))
        hour = date.split(' ')[1][:5]
        
        formatted_date = f'{day}/{month}/{year} {hour}'
        return formatted_date
    
    
    @staticmethod
    def search(db: DBManager, user_search: str) -> list:
        
        raw_search = db.search_for_location(user_search)
        names = []
        paths = []
        routes = []
        descriptions = []
        
        for name, path, route, description in raw_search:
            if name not in names:
                names.append(name)
                paths.append('.' + path)
                routes.append(route)
                descriptions.append(f'{description[:300]}...')
                
        treated_search = []
        for name, path, route, description in zip(names, paths, 
                                                  routes, descriptions):
            treated_search.append({
                'name': name,
                'path': path,
                'route': route,
                'description': description
            })
            
        return treated_search
    
    
    @staticmethod
    def search_names(db, user_search: str) -> list:
        
        untreated_names = db.search_location_names(user_search)
        
        names = []
        for name in untreated_names:
            names.append(name[0])
        
        return names