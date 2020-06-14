from django.db import models
from django.contrib.auth.models import User


class FavMovie(models.Model):
    """
    Model of favorite film users
    """
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.id)


class UserFavID(models.Model):
    fav_id = models.ManyToManyField(FavMovie, help_text="id for movie")
    username = models.CharField(max_length=200)

    def __str__(self):
        return " %s" % self.username

    def display_fav_id(self):
        return ', '.join([fav_id.id for fav_id in self.fav_id.all()[:3]])

    display_fav_id.short_description = "Favorite of user id "