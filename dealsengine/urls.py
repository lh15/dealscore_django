from django.urls import path

from .views import TriggerImport

urlpatterns = [
    path('trigger-import/<site_id>/', TriggerImport.as_view(), name='trigger_import'),
]
