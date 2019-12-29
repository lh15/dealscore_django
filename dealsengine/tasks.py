# tasks.py

from time import sleep
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from celery import shared_task

import json


from dealsengine.models import DealLink


# @shared_task this is for Celery, need to configure still
def crawl_dealnews():
    siteName = "Dealnews.com"
    print('Crawling DealNews.com data and creating links in database ..')
    req = Request('https://www.dealnews.com/?sort=time', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows  = bs.find_all('div', attrs={"class":"content-media content-view"})
    for row in rows:
        offerId = row.attrs.get("data-id", "")
        if DealLink.objects.filter(siteName=siteName, offerId=offerId).count() > 0:
            print("No new deals")
            break;
        imgUrl = row.find("img", attrs={"class":"lazy-img-bg"}).attrs.get("data-bg-src", "")
        offerPageLinkId = "overflow-menu-OFFER-" + offerId + "-0"
        offerPageLink = bs.find(id=offerPageLinkId).attrs.get("href", "")
        title = row.find("div", attrs={"class":"title"}).attrs.get("title", "")
        # Try get Category through JsonLd. Some offers don't have
        jsonLd = row.find('script', {'type': 'application/ld+json'}).text
        try:
            linkObj = json.loads(jsonLd)
            primaryCategory = linkObj.get("offers")[0].get("category", {}).get("alternateName", "")
        except (ValueError, TypeError) as error:
            print("error: " + str(error))
            primaryCategory = ""


        # print(row)
        print({'link': offerPageLink, 'imageUrl':imgUrl, 'siteName':siteName, 'primaryCategory':primaryCategory, 'description': title})

        # Create object in database from crawled data
        DealLink.objects.create(
            link = offerPageLink,
            description = title,
            imageUrl = imgUrl,
            siteName = siteName,
            offerId = offerId,
            primaryCategory = primaryCategory

        )
        sleep(1)