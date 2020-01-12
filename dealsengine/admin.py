from django.contrib import admin

# Register your models here.
from .models import *

myModels = [DealLink, DealSite, Vote, LinkClick, ThreadTask]  # iterable list
admin.site.register(myModels)