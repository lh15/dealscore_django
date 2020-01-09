# tasks.py

import time

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup, Tag

import json

from dealsengine.models import *
import threading



def longTask():
    while True:
        time.sleep(10)
        # task = ThreadTask(task="do_the_crawl")
        # task.save()
        # print("Received task", task.id)
        do_the_crawl()
        # task.is_done = True
        # print("Finishing task",task.id)
        # task.save()


thread = threading.Thread(target=longTask)

def startThreadTask():
    time.sleep(5)
    if not thread.is_alive():
        thread.setDaemon(True)
        thread.start()
    else:
        print("Thread is running")



def crawl_dealnews():
    site_name = "Dealnews.com"
    deal_site = DealSite.objects.get(site_name=site_name)
    print('Crawling DealNews.com data and creating links in database ..')
    req = Request(deal_site.primary_crawl_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows = bs.find_all('div', attrs={"class": "content-media content-view"})
    for row in rows:
        offer_id = row.attrs.get("data-id", "")

        if DealLink.objects.filter(site=deal_site, offer_id=offer_id).count() > 0:
            print("Not a new deal")
            continue; #consider break; to stop the loop
        img_url = row.find("img", attrs={"class": "lazy-img-bg"}).attrs.get("data-bg-src", "")
        offer_page_link_id = "overflow-menu-OFFER-" + offer_id + "-0"
        offer_page_link = bs.find(id=offer_page_link_id).attrs.get("href", "")
        title = row.find("div", attrs={"class": "title"}).attrs.get("title", "")

        # Try get Category and Subtitle price was through JsonLd. Some offers don't have
        try:
            callout_contents = row.find("div", attrs={"class": "callout"}).contents
            callout_curr_price = callout_contents[0].strip()
            if len(callout_contents) > 1 and isinstance(callout_contents[1], Tag):
                callout_price_was = " was " + callout_contents[1].get_text()
            else:
                callout_price_was = ""
            secondary_callout = row.find("div", attrs={"class": "secondary-callout"}).get_text()
            subtitle = callout_curr_price + callout_price_was + " - " + secondary_callout

        except Exception as error:
            print("error: " + str(error))
            subtitle = ""

        try:
            json_ld = row.find('script', {'type': 'application/ld+json'}).text
            link_obj = json.loads(json_ld)
            primary_category = link_obj.get("offers")[0].get("category", {}).get("alternateName", "")

        except Exception as error:
            print("error: " + str(error))
            primary_category = ""

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
        time.sleep(1)



def crawl_slickdeals():
    site_name = "Slickdeals.net"
    deal_site = DealSite.objects.get(site_name=site_name)
    print('Crawling Slickdeals.net data and creating links in database ..')
    req = Request(deal_site.primary_crawl_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows = bs.find_all('li', attrs={"class": "altDeal"})
    for row in rows:
        offer_id = row.attrs.get("data-threadid", "")

        if DealLink.objects.filter(site=deal_site, offer_id=offer_id).count() > 0:
            print("Not a new deal")
            continue; #consider break; to stop the loop
        try:
            img_url = row.find("div", attrs={"class": "imageContainer"}).img.attrs.get("data-original","")
        except Exception as error:
            print("error: " + str(error))
            continue
        offer_page_link = "https://slickdeals.net" + row.find("a", attrs={"class": "itemTitle"}).attrs.get("href", "")
        title = row.find("a", attrs={"class": "itemTitle"}).text

        print(
            {'link': offer_page_link, 'imageUrl': img_url, 'site_name': site_name,
             'description': title})
        # Create object in database from crawled data
        DealLink.objects.create(
            link=offer_page_link,
            title=title,
            sub_title="",
            image_url=img_url,
            site=deal_site,
            offer_id=offer_id,
            primary_category=""

        )
        time.sleep(1)


def crawl_krazy_coupon_lady():
    return

def crawl_hip2save():
    return

def do_the_crawl():
    crawl_dealnews()
    time.sleep(5)
    crawl_slickdeals()
    time.sleep(5)
    crawl_hip2save()
    time.sleep(5)
    crawl_krazy_coupon_lady()
    time.sleep(5)
    return
