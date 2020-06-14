from django.contrib import admin
from .models import FavMovie, UserFavID

# Register your models here.

admin.site.register(FavMovie)
admin.site.register(UserFavID)