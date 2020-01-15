from django.contrib import admin

# Register your models here.
from .models import *


class DealLinkAdmin(admin.ModelAdmin):
    readonly_fields = ('imported_at', 'import_date')

    class Meta:
        model = DealLink


admin.site.register(DealLink, DealLinkAdmin)


otherModels = [DealSite, Vote, LinkClick, ThreadTask]
admin.site.register(otherModels)
