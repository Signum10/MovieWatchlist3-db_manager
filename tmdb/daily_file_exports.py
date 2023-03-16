# https://developers.themoviedb.org/3/getting-started/daily-file-exports

import urllib.request
import gzip
import json
from io import BytesIO

categories = {
    'Movies': 'movie',
    'TV Series': 'tv_series',
    'People': 'person',
    'Collections': 'collection',
    'TV Networks': 'tv_network',
    'Keywords': 'keyword',
    'Production Companies': 'production_company',
}

def get_category_ids(category, year, month, day):
    url = f"http://files.tmdb.org/p/exports/{categories[category]}_ids_{month:02}_{day:02}_{year:04}.json.gz"
    ids = {}

    print(f'Downloading, decompressing and parsing {url}')
    with gzip.open(BytesIO(urllib.request.urlopen(url).read())) as f:
        for line in f.readlines():
            json_data = json.loads(line)
            ids[json_data['id']] = {k: v for k, v in json_data.items() if k != 'id'}

    print('Done')
    return ids
