import pytz
from django.db import models
from django.db.models import *
from datetime import date, timedelta

from dealscore import settings
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

    image_url = models.CharField(max_length=300)
    site = models.ForeignKey(DealSite, on_delete=CASCADE)
    offer_id = models.CharField(max_length=300)
    primary_category = models.CharField(max_length=300, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True, blank=True)
    import_date = models.DateField(auto_now_add=True, blank=True)
    link_post_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    score = models.IntegerField(default=0) # aggregate of the below 3 fields

    # upvotes = models.ManyToManyField(User, through='Upvote')

    highest_score = None

    class Meta:
        unique_together = ("site", "offer_id",)
        indexes = [
            models.Index(fields=['import_date', 'score']),
        ]

    def __str__(self):
        return self.imported_at.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S") + " - " + self.link

    def recalculate_score(self):
        sum = Vote.objects.filter(link=self).aggregate(Sum('vote'))
        self.score = sum.get("vote__sum", 0)
        self.save()
        DealLink.highest_score = DealLink.objects.select_related() \
            .filter(active=True, import_date__gt=date.today() - timedelta(days=7)) \
            .order_by('-score')[:1][0].score


    @property
    def was_posted_today(self):
        return self.import_date == date.today()

    @property
    def get_hotness_score(self):
        scoree = self.score
        if DealLink.highest_score is None:
            DealLink.highest_score = DealLink.objects.select_related() \
                                         .filter(active=True, import_date__gt=date.today() - timedelta(days=7)) \
                                         .order_by('-score')[:1][0].score
        if scoree== 0:
            scoree = 1
        divide_by = DealLink.highest_score if DealLink.highest_score > 0 else 1
        return int((scoree / divide_by) * 100)

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