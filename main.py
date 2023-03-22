import tmdb.api as api
import tmdb.daily_file_exports as tmdb_daily_file

IMG_BASE_URL = ""
IMG_POSTER_SIZE = 'w92'
IMG_STILL_SIZE = 'w92'

def get_api_config():
    global IMG_BASE_URL, IMG_POSTER_SIZE

    api_config = api.get_api_configuration()

    IMG_BASE_URL = api_config['images']['secure_base_url']

    if IMG_POSTER_SIZE not in api_config['images']['poster_sizes']:
        raise Exception(f'Counting on {IMG_POSTER_SIZE} poster size which is not available anymore')
    
    if IMG_STILL_SIZE not in api_config['images']['still_sizes']:
        raise Exception(f'Counting on {IMG_STILL_SIZE} still size which is not available anymore')

def get_movie_info(movie_id):
    global IMG_BASE_URL, IMG_POSTER_SIZE
    images = {}

    movie_details = api.get_movie_details(movie_id)
    movie_image = movie_details['poster_path']

    if movie_image:
        images[movie_image] = api.get_image(IMG_BASE_URL, IMG_POSTER_SIZE, movie_image)
    
    movie_info = {
        'id': movie_details['id'],
        'imdb_id': movie_details['imdb_id'],
        'title': movie_details['original_title'],
        'image': movie_image,
        'description': movie_details['overview'],
        'status': movie_details['status'],
        'release_date': movie_details['release_date'],
        'runtime_minutes': movie_details['runtime'],
        'popularity': movie_details['popularity'],
        'vote_average': movie_details['vote_average'],
        'vote_count': movie_details['vote_count']
    }

    return movie_info, images

def get_tv_info(tv_id):
    global IMG_BASE_URL, IMG_POSTER_SIZE
    images = {}

    tv_details = api.get_tv_details(tv_id, append_to_response='external_ids')
    tv_image = tv_details['poster_path']

    if tv_image:
        images[tv_image] = api.get_image(IMG_BASE_URL, IMG_POSTER_SIZE, tv_image)

    tv_info = {
        'id': tv_details['id'],
        'imdb_id': tv_details['external_ids']['imdb_id'],
        'title': tv_details['original_name'],
        'image': tv_image,
        'description': tv_details['overview'],
        'status': tv_details['status'],
        'first_air_date': tv_details['first_air_date'],
        'last_air_date': tv_details['last_air_date'],
        'popularity': tv_details['popularity'],
        'vote_average': tv_details['vote_average'],
        'vote_count': tv_details['vote_count']
    }

    season_infos = []
    episode_infos = []

    for season_entry in tv_details['seasons']:
        season_details = api.get_tv_season_details(tv_id, season_entry['season_number'])
        season_id = season_details['id']
        season_number = season_details['season_number']
        season_image = season_details['poster_path']

        if season_image:
            images[season_image] = api.get_image(IMG_BASE_URL, IMG_POSTER_SIZE, season_image)

        season_info = {
            'id': season_id,
            'tv_id': tv_id,
            'order': season_number,
            'title': season_details['name'],
            'image': season_image,
            'description': season_details['overview'],
            'air_date': season_details['air_date']
        }

        season_infos.append(season_info)

        for episode_entry in season_details['episodes']:
            episode_details = api.get_tv_episode_details(tv_id, season_number, episode_entry['episode_number'], append_to_response='external_ids')
            episode_id = episode_details['id']
            episode_number = episode_details['episode_number']
            episode_image = episode_details['still_path']

            if episode_image:
                images[episode_image] = api.get_image(IMG_BASE_URL, IMG_STILL_SIZE, episode_image)

            episode_info = {
                'id': episode_id,
                'season_id': season_id,
                'order': episode_number,
                'imdb_id': episode_details['external_ids']['imdb_id'],
                'title': episode_details['name'],
                'image': episode_image,
                'description': episode_details['overview'],
                'air_date': episode_details['air_date'],
                'vote_average': episode_details['vote_average'],
                'vote_count': episode_details['vote_count']
            }

            episode_infos.append(episode_info)

    return tv_info, season_infos, episode_infos, images


get_api_config()

import pprint
pprint.pprint(get_tv_info(1399))
#pprint.pprint(get_movie_info(550))