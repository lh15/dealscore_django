from django.views.generic import TemplateView
from dealsengine import tasks
from dealsengine import models


class HomePageView(TemplateView):
    # tasks.crawl_dealnews()
    # print(models.DealLink.objects.all())

    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'