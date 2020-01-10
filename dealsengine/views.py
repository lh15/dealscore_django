from symbol import if_stmt

from django.db import IntegrityError
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .tasks import *
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Vote, DealLink, LinkClick


class TriggerImport(View):

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        if pk == 0:
            startThreadTask()
        if pk == 1:
            crawl_dealnews()
        if pk == 2:
            crawl_slickdeals()
        if pk == 3:
            crawl_krazy_coupon_lady()

        return HttpResponse('Hello, World!' + str(pk))


def _vote(request, pk, vote=None, unvote=False):
    assert not unvote and vote is not None or unvote and vote is None
    link = get_object_or_404(DealLink, pk=pk)
    if (not unvote) and (vote is not None):
        is_upvote = vote == 1
        votes = Vote.objects.filter(link=link, user=request.user)
        if request.method == "POST":
            try:
                if request.user.is_superuser:
                    # make configurable...
                    vote = 5 if is_upvote else -5
                Vote.objects.update_or_create(link=link, user=request.user, defaults={'vote':vote})
                link.recalculate_score()
            except IntegrityError as error:
                print(error)
                return HttpResponse("NOT OK")
            return HttpResponse("OK")
    if unvote:
        if request.method == "POST":
            Vote.objects.update_or_create(link=link, user=request.user, defaults={'vote':0})
            return HttpResponse("OK")


@csrf_exempt
@login_required
def upvote(request, pk):
    return _vote(request, pk, vote=1)


@csrf_exempt
@login_required
def downvote(request, pk):
    return _vote(request, pk, vote=-1)


@csrf_exempt
@login_required
def unvote(request, pk):
    return _vote(request, pk, unvote=True)

@csrf_exempt
def click_track(request, pk):
    link = get_object_or_404(DealLink, pk=pk)
    if request.user.is_authenticated:
        LinkClick.objects.create(user=request.user, link=link)
    else:
        LinkClick.objects.create(link=link)

    return HttpResponse("OK")
