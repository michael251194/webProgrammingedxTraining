from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category (models.Model):
    categoryName = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.categoryName}"

class bids(models.Model):
    bids = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name="user_bid")
    def __str__(self):
        return f"{self.bids}"

class auction_list(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    imageUrl = models.CharField(max_length=1000)
    price = models.ForeignKey(bids, on_delete=models.CASCADE,blank=True, null=True, related_name="bids_auSction")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchList = models.ManyToManyField(User, blank=True, null=True,related_name="auctionWatchList")
    def __str__(self):
        return f"{self.title}"

class comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name="author")
    listing = models.ForeignKey(auction_list, on_delete=models.CASCADE, blank=True, null=True,  related_name="listing")
    message = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.author} comment on {self.listing}"




