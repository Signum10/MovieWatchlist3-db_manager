import tmdb.api as api

class TMDb:
    def __init__(self):
        api_config = api.get_configuration()

        self.IMG_BASE_URL = api_config['images']['secure_base_url']
        self.IMG_SIZE = 'w185'

        if self.IMG_SIZE not in api_config['images']['poster_sizes']:
            raise Exception(f'Expected poster_sizes to also include {self.IMG_SIZE}')
        
        if self.IMG_SIZE not in api_config['images']['still_sizes']:
            raise Exception(f'Expected still_sizes to also include {self.IMG_SIZE}')

    def get_images(self, image_paths):
        images = {}

        for image_path in image_paths:
            if image_path:
                images[image_path] = api.get_image(self.IMG_BASE_URL, self.IMG_SIZE, image_path)

        return images

    def get_movie_info(self, movie_id):
        details = api.get_movie(movie_id)
        
        info = {
            'id': details['id'],
            'imdb_id': details['imdb_id'],
            'title': details['original_title'],
            'image_path': details['poster_path'],
            'description': details['overview'],
            'status': details['status'],
            'release_date': details['release_date'],
            'runtime_minutes': details['runtime'],
            'popularity': details['popularity'],
            'vote_average': details['vote_average'],
            'vote_count': details['vote_count']
        }

        return info
    
    def get_tv_info(self, tv_id):
        details = api.get_tv(tv_id, append_to_response='external_ids')

        info = {
            'id': details['id'],
            'imdb_id': details['external_ids']['imdb_id'],
            'title': details['original_name'],
            'image_path': details['poster_path'],
            'description': details['overview'],
            'status': details['status'],
            'first_air_date': details['first_air_date'],
            'last_air_date': details['last_air_date'],
            'popularity': details['popularity'],
            'vote_average': details['vote_average'],
            'vote_count': details['vote_count']
        }

        return info, [entry['season_number'] for entry in details['seasons']]
    
    def get_season_info(self, tv_id, season_number):
        details = api.get_season(tv_id, season_number)

        info = {
            'id': details['id'],
            'title': details['name'],
            'image_path': details['poster_path'],
            'description': details['overview'],
            'air_date': details['air_date']
        }

        return info, [entry['episode_number'] for entry in details['episodes']]
    
    def get_episode_info(self, tv_id, season_number, episode_number):
        details = api.get_episode(tv_id, season_number, episode_number, append_to_response='external_ids')

        info = {
            'id': details['id'],
            'imdb_id': details['external_ids']['imdb_id'],
            'title': details['name'],
            'image_path': details['still_path'],
            'description': details['overview'],
            'air_date': details['air_date'],
            'vote_average': details['vote_average'],
            'vote_count': details['vote_count']
        }

        return info
    
    def get_movie_full_info(self, movie_id):
        movie_info = self.get_movie_info(movie_id)

        return movie_info, self.get_images([movie_info['image_path']])
        
    def get_tv_full_info(self, tv_id):
        season_infos = []
        episode_infos = []
        image_paths = []

        tv_info, season_numbers = self.get_tv_info(tv_id)
        image_paths.append(tv_info['image_path'])

        for season_number in season_numbers:
            season_info, episode_numbers = self.get_season_info(tv_id, season_number)

            season_info['tv_id'] = tv_id
            season_info['order'] = season_number
            season_infos.append(season_info)
            image_paths.append(season_info['image_path'])

            for episode_number in episode_numbers:
                episode_info = self.get_episode_info(tv_id, season_number, episode_number)

                episode_info['season_id'] = season_info['id']
                episode_info['order'] = episode_number
                episode_infos.append(episode_info)
                image_paths.append(episode_info['image_path'])

        return tv_info, season_infos, episode_infos, self.get_images(image_paths)
