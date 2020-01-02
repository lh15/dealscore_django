from django.urls import path

from .views import downvote, upvote, unvote, TriggerImport, click_track

urlpatterns = [
    path('trigger-import/<site_id>/', TriggerImport.as_view(), name='trigger_import'),
    path('upvote/<int:pk>', upvote, name="upvote"),
    path('downvote/<int:pk>', downvote, name="downvote"),
    path('unvote/<int:pk>', unvote, name="unvote"),
    path('click_track/<int:pk>', click_track, name="click_track"),
]
