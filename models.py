from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class AuctionList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2000)
    category = models.CharField(max_length=64)
    image = models.URLField(default="")
    bid = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    #xy = models.IntegerField()


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authorComment")
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="aution")


class WatchList(models.Model):
    auction_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")


class Bid(models.Model):
    bid_a_id = models.IntegerField()
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_info")
    bid = models.FloatField()


class ClosedAuction(models.Model):
    close_a_id = models.IntegerField()
    close_u_id = models.IntegerField()
