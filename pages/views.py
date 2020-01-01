from django.views.generic import TemplateView
from dealsengine import tasks
from dealsengine import models
from collections import Set


class HomePageView(TemplateView):
    # tasks.crawl_dealnews()
    # print(models.DealLink.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        deal_links = models.DealLink.objects.select_related().all()
        context['deal_links'] = deal_links
        user_upvotes_link_ids = models.Vote.objects.filter(user=self.request.user).values_list('link_id', flat=True)
        context['user_upvotes_link_ids'] = list(user_upvotes_link_ids)
        return context
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'