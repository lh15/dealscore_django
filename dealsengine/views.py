from symbol import if_stmt

from django.http import HttpResponse
from django.views import View
from .tasks import crawl_dealnews

class TriggerImport(View):

    def get(self, request, site_id,  *args, **kwargs):
        print(site_id)
        if site_id == "dealnews.com":
            crawl_dealnews()

        return HttpResponse('Hello, World!' + site_id)

