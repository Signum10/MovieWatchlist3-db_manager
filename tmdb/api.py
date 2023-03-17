# https://developers.themoviedb.org/3/getting-started/introduction

import urllib.parse
import urllib.request
from decouple import config

API_READ_ACCESS_TOKEN = config("API_READ_ACCESS_TOKEN")

def get(path, path_params=None, **kwargs):
    url = f"https://api.themoviedb.org/3/{path}"

    if kwargs:
        url += "?" + '&'.join([f"{k}={v}" for k, v in kwargs.items()])

    url = urllib.parse.quote(url, safe=':/?&=')

    print(url)

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
