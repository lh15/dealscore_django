from django.db import models


class DealLink(models.Model):
    link = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200)
    siteName = models.CharField(max_length=100)  # TODO: make integer ID
    offerId = models.CharField(max_length=100)
    primaryCategory = models.CharField(max_length=100)

    class Meta:
        unique_together = ("siteName", "offerId",)

    def __str__(self):
        return self.link
