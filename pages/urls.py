from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url

from .views import HomePageView, AboutPageView, DiapersPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('diapers/', DiapersPageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

]