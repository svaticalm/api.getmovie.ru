from django.urls import path
from . import views


urlpatterns = [
    path("", views.index),
]

urlpatterns += [
    path("auth/", views.auth_users),
    path("logout/", views.logout_view),
]
urlpatterns += [
    path("login/", views.log_in)
]