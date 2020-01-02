from django.db import models
from django.db.models import *

from users.models import CustomUser


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

    # upvotes = models.ManyToManyField(User, through='Upvote')

    class Meta:
        unique_together = ("site", "offer_id",)

    def __str__(self):
        return self.link

    def recalculate_score(self):
        sum = Vote.objects.filter(link=self).aggregate(Sum('vote'))
        self.score = sum.get("vote__sum", 0)
        self.save()

class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
    # vote = None # -1 | 0 | 1 --> BooleanField(default=None, null=True)??
    vote = models.SmallIntegerField(default=1)
    user = models.ForeignKey(CustomUser, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("link", "user",)

class LinkClick(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='link_clicks', on_delete=models.CASCADE, blank = True, null = True)
