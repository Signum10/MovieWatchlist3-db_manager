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

    def _get_movie_info(self, data, source):
        info = {
            'id': data['id'],
            'title': data['original_title'],
            'image_path': data['poster_path'],
            'description': data['overview'],
            'release_date': data['release_date'],
            'popularity': data['popularity'],
            'vote_average': data['vote_average'],
            'vote_count': data['vote_count']
        }

        if source == 'details':
            info.update({
                'imdb_id': data['imdb_id'],
                'status': data['status'],
                'runtime_minutes': data['runtime'],
                'genre_ids': [entry['id'] for entry in data['genres']]
            })
        elif source == 'search':
            info.update({
                'genre_ids': data['genre_ids']
            })

        return info
    
    def _get_tv_info(self, data, source):
        info = {
            'id': data['id'],
            'title': data['original_name'],
            'image_path': data['poster_path'],
            'description': data['overview'],
            'first_air_date': data['first_air_date'],
            'popularity': data['popularity'],
            'vote_average': data['vote_average'],
            'vote_count': data['vote_count']
        }

        if source == 'details':
            info.update({
                'imdb_id': data['external_ids']['imdb_id'],
                'status': data['status'],
                'episode_runtime_minutes': data['episode_run_time'][0],
                'last_air_date': data['last_air_date'],
                'genre_ids': [entry['id'] for entry in data['genres']],
                'season_numbers': [entry['season_number'] for entry in data['seasons']]
            })
        elif source == 'search':
            info.update({
                'genre_ids': data['genre_ids']
            })

        return info
    
    def _get_season_info(self, data, tv_id):
        info = {
            'id': data['id'],
            'tv_id': tv_id,
            'season_number': data['season_number'],
            'title': data['name'],
            'image_path': data['poster_path'],
            'description': data['overview'],
            'air_date': data['air_date'],
            'episode_numbers': [entry['episode_number'] for entry in data['episodes']]
        }

        return info
    
    def _get_episode_info(self, data, season_id):
        info = {
            'id': data['id'],
            'season_id': season_id,
            'episode_number': data['episode_number'],
            'imdb_id': data['external_ids']['imdb_id'],
            'title': data['name'],
            'image_path': data['still_path'],
            'description': data['overview'],
            'air_date': data['air_date'],
            'vote_average': data['vote_average'],
            'vote_count': data['vote_count']
        }

        return info

    def _get_all_pages(self, method, **kwargs):
        results = []
        current_page = 1
        total_pages = 1

        while current_page <= total_pages:
            kwargs['page'] = current_page
            response = method(**kwargs)

            results += response['results']
            current_page += 1
            total_pages = response['total_pages']

        return results

    def get_images(self, image_paths):
        images = {}

        for image_path in image_paths:
            if image_path:
                images[image_path] = api.get_image(self.IMG_BASE_URL, self.IMG_SIZE, image_path)

        return images

    def get_genres(self):
        methods = [api.get_genre_movie_list, api.get_genre_tv_list]

        return [{entry['id']:entry['name'] for entry in method()['genres']} for method in methods]
    
    def get_changes(self, start_date, end_date):
        methods = [api.get_movie_changes, api.get_tv_changes]
        kwargs = {'start_date': start_date, 'end_date': end_date}

        return [[entry['id'] for entry in self._get_all_pages(method, **kwargs)] for method in methods]
    
    def get_movie(self, movie_id):
        return self._get_movie_info(api.get_movie(movie_id), 'details')
        
    def get_tv(self, tv_id):
        tv_info = self._get_tv_info(api.get_tv(tv_id, append_to_response='external_ids'), 'details')
        season_infos = [self._get_season_info(api.get_season(tv_id, season_number), tv_id) for season_number in tv_info['season_numbers']]
        episode_infos = [self._get_episode_info(api.get_episode(tv_id, season_info['season_number'], episode_number, append_to_response='external_ids'), season_info['id']) for season_info in season_infos for episode_number in season_info['episode_numbers']]

        return tv_info, season_infos, episode_infos

    def search(self, query):
        methods = [(self._get_movie_info, api.search_movie), (self._get_tv_info, api.search_tv)]

        return [[m1(data, 'search') for data in self._get_all_pages(m2, query=query)] for m1, m2 in methods]
