from django.db import models
from django.contrib.auth.models import User


class Fav(models.Model):
    favid = models.IntegerField()

    def __str__(self):
        return str(self.favid)

class UserFav(models.Model):
    """
    Model of favorite film users
    """
    userid = models.IntegerField()
    favid = models.IntegerField()

    def __str__(self):
        return str(self.userid) + str(self.favid)

