from django.contrib.auth.models import User
from django.db import models
from django.db.models import *


class DealSite(models.Model):
    site_name = models.CharField(max_length=100)
    primary_crawl_url = models.CharField(max_length=100)
    crawl_interval_mins = models.IntegerField(default=15)

    def __str__(self):
        return self.site_name


class DealLink(models.Model):
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)

    image_url = models.CharField(max_length=200)
    site = models.ForeignKey(DealSite, on_delete=SET_DEFAULT, default=0)
    offer_id = models.CharField(max_length=100)
    primary_category = models.CharField(max_length=100)
    import_date = models.DateTimeField(auto_now=True, db_index=True)
    link_post_date = models.DateTimeField(null=True)

    score = models.IntegerField(default=0) # aggregate of the below 3 fields

    # see comment below by the Models
    # upvotes = models.ManyToManyField(User, through='Upvote')
    # editor_upvotes = models.ManyToManyField(User, through='EditorUpvote')
    # deallink_posts = models.ManyToManyField(User, through='DealPosts')
    # will also need to add a deal_id to count dups

    class Meta:
        unique_together = ("site", "offer_id",)

    def __str__(self):
        return self.link


# Models for the 3 components of the dealScore.
# 1. User upvotes
# 2. admin upvotes
# 3. Number of times the same deal was posts around
# class Upvote(models.Model):
#     link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='upvotes', on_delete=models.CASCADE)
#
#
# class EditorUpvote(models.Model):
#     link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='editor_upvotes', on_delete=models.CASCADE)


# class DealPosts(models.Model):
#     link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
#     site = models.ForeignKey(DealSite, related_name='deallink_posts', on_delete=models.CASCADE)
