from datetime import datetime, date, timedelta

from django.views.generic import TemplateView
from dealsengine import tasks
from dealsengine import models
from collections import Set


class HomePageView(TemplateView):
    # tasks.crawl_dealnews()
    # print(models.DealLink.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        deal_links = models.DealLink.objects.select_related()\
            .filter(active=True, import_date__gt=date.today()-timedelta(days=7))\
            .order_by('-import_date', '-score', '-title')
        context['deal_links'] = deal_links
        context['page_title'] = 'Baby and Kids deals from around the web, ranked!'
        if self.request.user.is_authenticated:
            user_upvotes_link_ids = models.Vote.objects.filter(user=self.request.user, vote__gte=1).values_list('link_id', flat=True)
            context['user_upvotes_link_ids'] = list(user_upvotes_link_ids)
            user_downvotes_link_ids = models.Vote.objects.filter(user=self.request.user, vote__lte=-1).values_list('link_id', flat=True)
            context['user_downvotes_link_ids'] = list(user_downvotes_link_ids)
        return context
    template_name = 'pages/home.html'

class DiapersPageView(TemplateView):
    # tasks.crawl_dealnews()
    # print(models.DealLink.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(DiapersPageView, self).get_context_data(*args, **kwargs)
        deal_links = models.DealLink.objects.select_related()\
            .filter(active=True, import_date__gt=date.today()-timedelta(days=7), title__icontains='diaper').exclude(title__icontains='bag')\
            .order_by('-import_date', '-score', '-title')
        context['deal_links'] = deal_links
        context['page_title'] = 'Deals on Diapers from around the web, ranked!'
        if self.request.user.is_authenticated:
            user_upvotes_link_ids = models.Vote.objects.filter(user=self.request.user, vote__gte=1).values_list('link_id', flat=True)
            context['user_upvotes_link_ids'] = list(user_upvotes_link_ids)
            user_downvotes_link_ids = models.Vote.objects.filter(user=self.request.user, vote__lte=-1).values_list('link_id', flat=True)
            context['user_downvotes_link_ids'] = list(user_downvotes_link_ids)
        return context
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'