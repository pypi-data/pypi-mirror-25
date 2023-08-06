import urllib
import requests
from podcasts.constants import ITUNES_SEARCH_URL, ITUNES_LOOKUP_URL
from podcasts.api import API
from podcasts.models.series import Series

def search_podcast_series(query):
  params = {'entity': 'podcast', 'limit': 200, 'term': query}
  encoded_params = urllib.urlencode(params)
  results = API().\
    req_itunes(ITUNES_SEARCH_URL + encoded_params).\
    json()['results']
  return [
      Series.from_itunes_json(j)
      for j in results
      if j.get('feedUrl') is not None
  ]

def get_series_by_ids(ids):
    ids_with_coms = ','.join(ids)
    id_param = {'id': ids_with_coms}
    results = API().\
      req_itunes(ITUNES_LOOKUP_URL + urllib.urlencode(id_param)).\
      json()['results']
    return [
        Series.from_itunes_json(j)
        for j in results
        if j.get('feedUrl') is not None
    ]
