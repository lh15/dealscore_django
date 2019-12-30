# tasks.py

from time import sleep
import re

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from celery import shared_task

import json

from dealsengine.models import *


# @shared_task this is for Celery, need to configure still
def crawl_dealnews():
    site_name = "Dealnews.com"
    print('Crawling DealNews.com data and creating links in database ..')
    req = Request('https://www.dealnews.com/?sort=time', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows = bs.find_all('div', attrs={"class": "content-media content-view"})
    for row in rows:
        offer_id = row.attrs.get("data-id", "")
        deal_site = DealSite.objects.get(site_name=site_name)
        if DealLink.objects.filter(site=deal_site, offer_id=offer_id).count() > 0:
            print("No new deals")
            break;
        img_url = row.find("img", attrs={"class": "lazy-img-bg"}).attrs.get("data-bg-src", "")
        offer_page_link_id = "overflow-menu-OFFER-" + offer_id + "-0"
        offer_page_link = bs.find(id=offer_page_link_id).attrs.get("href", "")
        title = row.find("div", attrs={"class": "title"}).attrs.get("title", "")

        # Try get Category through JsonLd. Some offers don't have
        try:
            json_ld = row.find('script', {'type': 'application/ld+json'}).text
            link_obj = json.loads(json_ld)
            primary_category = link_obj.get("offers")[0].get("category", {}).get("alternateName", "")
            callout = row.find("div", attrs={"class": "callout"}).get_text().strip()
            secondary_callout = row.find("div", attrs={"class": "secondary-callout"}).get_text()
            subtitle = callout + " - " + secondary_callout
        except Exception as error:
            print("error: " + str(error))
            primary_category = ""
            subtitle = ""

        # print(row)
        print({'link': offer_page_link, 'imageUrl': img_url, 'site_name': site_name, 'primaryCategory': primary_category,
               'description': title})

        # Create object in database from crawled data
        DealLink.objects.create(
            link=offer_page_link,
            title=title,
            sub_title=subtitle,
            image_url=img_url,
            site=deal_site,
            offer_id=offer_id,
            primary_category=primary_category

        )
        sleep(1)
