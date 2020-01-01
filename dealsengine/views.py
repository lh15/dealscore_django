from symbol import if_stmt

from django.db import IntegrityError
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .tasks import crawl_dealnews
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Vote, DealLink


class TriggerImport(View):

    def get(self, request, site_id, *args, **kwargs):
        print(site_id)
        if site_id == "dealnews.com":
            crawl_dealnews()

        return HttpResponse('Hello, World!' + site_id)


def _vote(request, pk, vote=None, unvote=False):
    assert not unvote and vote is not None or unvote and vote is None
    link = get_object_or_404(DealLink, pk=pk)
    if (not unvote) and (vote is not None):
        votes = Vote.objects.filter(link=link, user=request.user)
        if request.method == "POST":
            try:
                vote = Vote(vote=vote, link=link, user=request.user)
                vote.save()
            except IntegrityError:
                return HttpResponse("NOT OK, already voted %s" % (vote.pk))
            return HttpResponse("OK %s" % (vote.pk))
    if unvote:
        if request.method == "POST":
            Vote.objects.filter(link=link, user=request.user).update(vote=vote, link=link, user=request.user)
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
    return _vote(request, pk, vote=0, unvote=True)
