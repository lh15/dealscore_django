# tasks.py

from time import sleep
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from celery import shared_task

import json

from pkg_resources import non_empty_lines

from dealsengine.models import DealLink


@shared_task
# do some heavy stuff
def crawl_dealnews():
    print('Crawling data and creating objects in database ..')
    req = Request('https://www.dealnews.com/', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    # Find first 5 table rows
    rows = bs.findAll('script', {'type': 'application/ld+json'})
    for row in rows:
        jsonLd = row.text
        try:
            linkObj = json.loads(jsonLd)
        except ValueError:
            print("error")
            break
        print(row)
        link = linkObj["url"]
        imageUrl = linkObj["image"]["contentUrl"]
        siteName = "Dealnews.com"
        primaryCategory = linkObj["category"]["name"]
        description = linkObj["description"]

        print({'link': link, 'imageUrl':imageUrl, 'siteName':siteName, 'primaryCategory':primaryCategory, 'description': description})

        # Create object in database from crawled data
        DealLink.objects.create(
            link = link,
            description = description,
            imageUrl = imageUrl,
            siteName = siteName,
            primaryCategory = primaryCategory

        )
        sleep(1)


# crawl_dealnews()
