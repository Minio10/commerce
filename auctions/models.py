from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass



class Listing(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length= 128)
    start_value = models.IntegerField()
    category = models.CharField(max_length=64)
    image_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    flag_active = models.IntegerField(default = 0) # 0 - for active 1 - closed auction
    winner = models.CharField(max_length=50, null = True, blank = True,default = None)

class Bid(models.Model):

    value = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "object")

class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length= 300)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "item")

class Watchlist(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "watch")
