from django.db import models
from django.db.models import *
from datetime import date

from users.models import CustomUser


class DealSite(models.Model):
    site_name = models.CharField(max_length=100)
    primary_crawl_url = models.CharField(max_length=100)
    crawl_interval_mins = models.IntegerField(default=15)
    color_hex = models.CharField(max_length=6)

    def __str__(self):
        return self.site_name


class DealLink(models.Model):
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    sub_title = models.CharField(max_length=500, blank=True)

    image_url = models.CharField(max_length=200)
    site = models.ForeignKey(DealSite, on_delete=SET_DEFAULT, default=0)
    offer_id = models.CharField(max_length=100)
    primary_category = models.CharField(max_length=100, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True, blank=True)
    import_date = models.DateField(auto_now_add=True, blank=True)
    link_post_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField()

    score = models.IntegerField(default=0) # aggregate of the below 3 fields

    # upvotes = models.ManyToManyField(User, through='Upvote')

    class Meta:
        unique_together = ("site", "offer_id",)
        indexes = [
            models.Index(fields=['import_date', 'score']),
        ]

    def __str__(self):
        return self.link

    def recalculate_score(self):
        sum = Vote.objects.filter(link=self).aggregate(Sum('vote'))
        self.score = sum.get("vote__sum", 0)
        self.save()

    @property
    def was_posted_today(self):
        return self.import_date == date.today()

class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
    # vote = None # -1 | 0 | 1 --> BooleanField(default=None, null=True)??
    vote = models.SmallIntegerField(default=1)
    user = models.ForeignKey(CustomUser, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("link", "user",)

    def __str__(self):
        return self.link.link

class LinkClick(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.ForeignKey(DealLink, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='link_clicks', on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.link.link


class ThreadTask(models.Model):
    task = models.CharField(max_length=30, blank=True, null=True)
    is_done = models.BooleanField(blank=False,default=False )

    def __str__(self):
        return self.task