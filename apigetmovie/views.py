from django.shortcuts import render
from django.template.response import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationUsersForm, LoginFormUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
from apigetmovie.api.request_api import RandomFilm
from django.http import QueryDict
from json import dumps
from .models import Fav, UserFav
from urllib.parse import parse_qs


def index(request, id=-1):
    if request.method == 'POST':
        response_ajax = request.read().decode("UTF-8")
        type_of_request = QueryDict(response_ajax).get('random')
        type_ = QueryDict(response_ajax).get('type')
        film = RandomFilm(type_)

        if type_of_request == 'false':
            res = film.get_film_for_id(id)
        else:
            res = film.get_film()

        if res is False:
            return HttpResponse(dumps({'error_api': 'Извините, но произошла неизвестная ошибка. Попробуйте еще раз'}))

        res.update({"error_api": ""})
        return HttpResponse(dumps(res))

    return render(request, 'index.html')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        errors = {}
        response_ajax = parse_qs(request.read().decode("UTF-8"))
        username = response_ajax['username'][0]
        email = response_ajax['email'][0]
        password = response_ajax['password'][0]
        password_repeat = response_ajax['password-repeat'][0]

        exist_email = User.objects.filter(email=email).count()
        if exist_email > 0:
            errors.update({'signup_error_email': 'данный email уже используется',})

        exist_username = User.objects.filter(username=username).count()

        if exist_username > 0:
            errors.update({'signup_error_username': 'пользователь с таким именем уже существует',})

        if password != password_repeat:
            errors.update({'signup_error_password': 'пароли не совпадают'})

        if errors != {}:
            res = dumps({'signup': False, 'errors': errors})
            return HttpResponse(res)

        user = User.objects.create_user(username, email, password)
        user.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return HttpResponse(dumps({'login': True, 'signup': True}))


    return HttpResponseRedirect('/')


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        response_ajax = parse_qs(request.read().decode("UTF-8"))
        username = response_ajax['username'][0]
        password = response_ajax['password'][0]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(dumps({'login': True}))
        else:
            return HttpResponse(dumps({'login': False}))

    return HttpResponseRedirect('/')


def get_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        return HttpResponse(dumps({'username': username, }))
    

def add_fav_id(request):

    if not request.user.is_authenticated:
        return HttpResponse(dumps({'fav_add': False, "authenticated": False}))

    if request.method == "POST":
        response_ajax = request.read().decode("UTF-8")
        id = QueryDict(response_ajax).get('filmId')
        type_ = QueryDict(response_ajax).get('type')
        userid = User.objects.get(username=request.user.username).id

        favid_or_not = Fav.objects.filter(favid=id).count()

        if favid_or_not == 0:
            Fav.objects.create(favid=id, type=type_)

        obj_ = UserFav.objects.filter(favid=id, userid=userid).count()

        if obj_ == 0:
            UserFav.objects.create(userid=userid, favid=id)
            result = get_list_favorite(request)
            result.update({'fav_add': True, "authenticated": True})

            return HttpResponse(dumps(result))
        return HttpResponse(dumps({'fav_add': False, "authenticated": True}))

    return HttpResponseRedirect('/')


def get_favs(request):

    if not request.user.is_authenticated:
        return HttpResponse(dumps({"authenticated": False}))

    if request.method == "POST":
        result = get_list_favorite(request)
        HttpResponse(dumps(result))

    return HttpResponseRedirect('/')


def get_list_favorite(request):
    userid = User.objects.get(username=request.user.username).id
    list_id = UserFav.objects.filter(userid=userid)
    result = {}
    i = 1
    for id in list_id:
        print(id.get_favid())
        type_ = Fav.objects.get(favid=id.get_favid()).get_type()
        print(type_)
        film = RandomFilm(type_).get_film_for_id(id.get_favid())

        res = {"id": id.get_favid(), "type": type_, "poster_path": film["poster_path"], "title": film["title"]}
        result.update({str(i): res})

    return result











