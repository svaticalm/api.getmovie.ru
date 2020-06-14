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
    fav_id = models.ManyToManyField(FavMovie)
    username = models.CharField(max_length=200)

    def __str__(self):
        return " %s" % self.username
