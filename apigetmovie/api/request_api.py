from urllib.request import urlopen
from urllib.parse import urlencode
from random import randint
import json

API_KEY = "7e00b848ffbb0a2bb957f6631e1ad255"
URL_API = "http://api.themoviedb.org/3/discover/movie?%s"
MAX_PAGE = 500


def get_response_json(language_list, **kwargs):
    rand_int = randint(1, MAX_PAGE)
    langs = ','.join(language_list)
    vars_req = {"api_key": API_KEY, "page": rand_int, "language": langs}
    vars_req.update(kwargs)
    variables_request = urlencode(vars_req)
    url = URL_API % variables_request
    res = urlopen(url).read().decode(encoding="UTF-8")

    if res is False:
        return False

    res_json = json.loads(res)

    try:
        if res_json['results'] is False:
            return False
    except KeyError:
        return False

    return res_json['results']


def get_movie(res):
    max_len = len(res)
    num = randint(1, max_len)
    film = res[num]
    movie_descriptions = film

    return movie_descriptions
