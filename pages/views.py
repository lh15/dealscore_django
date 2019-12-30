from django.views.generic import TemplateView
from dealsengine import tasks
from dealsengine import models


class HomePageView(TemplateView):
    # tasks.crawl_dealnews()
    # print(models.DealLink.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        dealLinks = models.DealLink.objects.all()
        context['dealLinks'] = dealLinks
        return context
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'