import tmdb.api as api
import tmdb.daily_file_exports as tmdb_daily_file

IMG_BASE_URL = ""
IMG_POSTER_SIZE = 'w92'

def get_api_config():
    global IMG_BASE_URL, IMG_POSTER_SIZE

    api_config = api.get_api_configuration()

    IMG_BASE_URL = api_config['images']['secure_base_url']

    if IMG_POSTER_SIZE not in api_config['images']['poster_sizes']:
        raise Exception(f'Counting on {IMG_POSTER_SIZE} poster size which is not available anymore')

def get_movie_info(movie_id):
    global IMG_BASE_URL, IMG_POSTER_SIZE

    details = api.get_movie_details(movie_id)

    return {
        'id': details['id'],
        'imdb_id': details['imdb_id'],
        'title': details['original_title'],
        'poster': api.get_image(IMG_BASE_URL, IMG_POSTER_SIZE, details['poster_path']),
        'description': details['overview'],
        'status': details['status'],
        'release_date': details['release_date'],
        'runtime_minutes': details['runtime'],
        'popularity': details['popularity'],
        'vote_average': details['vote_average'],
        'vote_count': details['vote_count']
    }

get_api_config()