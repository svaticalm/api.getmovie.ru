from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationUsersForm, LoginFormUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
from apigetmovie.api import request_api


def index(request):
    res = request_api.get_response_json(language_list=["ru",])

    if res is False:
        return render(request,
               'index.html',
               context={'error_api': 'Извините, но произошла неизвестная ошибка. Попробуйте еще раз'})

    movie_descriptions = request_api.get_movie(res)
    movie_descriptions.update({"error_api": ""})
    return render(request,
                  'index.html',
                  context=movie_descriptions)


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
