from urllib.request import urlopen
from urllib.parse import urlencode
from random import randint
import json


class RandomFilm:
    def __init__(self, type_, **kwargs):
        self.api_key = "7e00b848ffbb0a2bb957f6631e1ad255"
        self.url_api_discover = "http://api.themoviedb.org/3/discover/" + type_ + "?%s"
        self.url_api_detail = "http://api.themoviedb.org/3/" + type_ + "/%s?%s"
        self.max_page = 500
        self.type = type_
        self.vars_req = {"api_key": self.api_key, 'language': 'ru'}
        self.vars_req.update(kwargs)

    def __error_or_return_dict(self, res):
        if res is False:
            return False

        res = json.loads(res)
        try:
            if res['errors'] is True:
                return False
        except KeyError:
            pass

        return res

    def get_film(self):
        self.vars_req['page'] = randint(1, self.max_page)

        url = self.url_api_discover % urlencode(self.vars_req)  # добавляем критерии поиска в url
        res = urlopen(url).read().decode(encoding="UTF-8")  # читаем

        self.vars_req.pop('page')

        res = self.__error_or_return_dict(res)

        id = self.get_film_id(res['results'])

        res = self.get_detail(id)

        return res

    def get_detail(self, id):

        url = self.url_api_detail % (id, urlencode(self.vars_req))
        print(url)
        res = urlopen(url).read().decode(encoding="UTF-8")

        res = self.__error_or_return_dict(res)

        return res

    def get_film_id(self, res):
        max_len = len(res)
        num = randint(0, max_len - 1)
        film = res[num]
        movie_descriptions = film

        return movie_descriptions['id']


