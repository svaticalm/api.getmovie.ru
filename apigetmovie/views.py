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


def index(request):
    if request.method == 'POST':
        response_ajax = request.read().decode("UTF-8")
        type_ = QueryDict(response_ajax).get('type')
        film = RandomFilm(type_)
        res = film.get_film()

        if res is False:
            return HttpResponse(dumps({'error_api': 'Извините, но произошла неизвестная ошибка. Попробуйте еще раз'}))

        res.update({"error_api": ""})
        print(res)
        return HttpResponse(dumps(res))

    return render(request, 'index.html')


def auth_users(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RegistrationUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).count()
            if user is not 0:
                form.errors['email'] = ["такой пользователь уже существует"]
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect('/')

    else:
        form = RegistrationUsersForm()

    return render(request, 'auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def log_in(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginFormUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.errors['username'] = ["Пользователь не найден"]
    else:
        form = LoginFormUser()

    return render(request, 'login.html', {'form': form})
