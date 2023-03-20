# https://developers.themoviedb.org/3/getting-started/introduction

import urllib.parse
import urllib.request
import json
from decouple import config

def get(path, **kwargs):
    url = f"https://api.themoviedb.org/3/{path}"

    if kwargs:
        url += "?" + '&'.join([f"{k}={v}" for k, v in kwargs.items()])

    url = urllib.parse.quote(url, safe=':/?&=')
    headers = {
        'Authorization': f'Bearer {config("API_READ_ACCESS_TOKEN")}',
        'Content-Type': 'application/json;charset=utf-8'
    }

    print(f'API request {url}')
    response = urllib.request.urlopen(urllib.request.Request(url, None, headers))
    print(f'API request returned {response.status} {response.reason}')
    
    return json.loads(response.read())

def get_image(base_url, file_size, file_path):
    url = f"{base_url}{file_size}{file_path}"

    print(f'Fetch image {url}')
    response = urllib.request.urlopen(url)
    print(f'Fetch image returned {response.status} {response.reason}')
    
    return response.read()

# https://developers.themoviedb.org/3/configuration/get-api-configuration
def get_api_configuration():
    return get(f'configuration')

# https://developers.themoviedb.org/3/genres/get-movie-list
def get_movie_genres(**kwargs):
    return get(f'genre/movie/list', **kwargs)

# https://developers.themoviedb.org/3/genres/get-tv-list
def get_tv_genres(**kwargs):
    return get(f'genre/tv/list', **kwargs)

# https://developers.themoviedb.org/3/changes/get-movie-change-list
def get_movie_change_list(**kwargs):
    return get(f'movie/changes', **kwargs)

# https://developers.themoviedb.org/3/changes/get-tv-change-list
def get_tv_change_list(**kwargs):
    return get(f'tv/changes', **kwargs)

# https://developers.themoviedb.org/3/movies/get-movie-details
def get_movie_details(movie_id, **kwargs):
    return get(f'movie/{movie_id}', **kwargs)

# https://developers.themoviedb.org/3/tv/get-tv-details
def get_tv_details(tv_id, **kwargs):
    return get(f'tv/{tv_id}', **kwargs)

# https://developers.themoviedb.org/3/tv-seasons/get-tv-season-details
def get_tv_season_details(tv_id, season_number, **kwargs):
    return get(f'tv/{tv_id}/season/{season_number}', **kwargs)

# https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-details
def get_tv_episode_details(tv_id, season_number, episode_number, **kwargs):
    return get(f'tv/{tv_id}/season/{season_number}/episode/{episode_number}', **kwargs)

i = get_image('https://image.tmdb.org/t/p/', 'w500', '/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg')

