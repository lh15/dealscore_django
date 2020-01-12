# tasks.py
import os
import time

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup, Tag
from selenium import webdriver

import json

from dealscore.settings import CHROMEDRIVER_PATH, GOOGLE_CHROME_PATH
from dealsengine.models import *
import threading


def simple_crawl_task():
    while True:
        time.sleep(10)
        # task = ThreadTask(task="do_the_crawl")
        # task.save()
        # print("Received task", task.id)
        do_simple_crawl()
        # task.is_done = True
        # print("Finishing task",task.id)
        # task.save()


def selenium_crawl_task():
    while True:
        time.sleep(60)
        # task = ThreadTask(task="do_the_crawl")
        # task.save()
        # print("Received task", task.id)
        do_selenium_crawl()
        # task.is_done = True
        # print("Finishing task",task.id)
        # task.save()


def start_crawling_threads():
    start_simple_crawl_thread()
    start_selenium_crawl_thread()
    return


def start_simple_crawl_thread():
    simple_crawl_thread = threading.Thread(target=simple_crawl_task)
    try:
        if not simple_crawl_thread.is_alive():
            simple_crawl_thread.setDaemon(True)
            print("Starting start_simple_crawl_thread background thread")
            simple_crawl_thread.start()
        else:
            print("Thread is running")
    except Exception as error:
        print(error)
        print("Starting background thread AGAIN due to error")
        new_simple_crawl_thread = threading.Thread(target=simple_crawl_task)
        new_simple_crawl_thread.setDaemon(True)
        new_simple_crawl_thread.start()


def start_selenium_crawl_thread():
    selenium_crawl_thread = threading.Thread(target=selenium_crawl_task)
    try:
        if not selenium_crawl_thread.is_alive():
            selenium_crawl_thread.setDaemon(True)
            print("Starting start_selenium_crawl_thread background thread")
            selenium_crawl_thread.start()
        else:
            print("Thread is running")
    except Exception as error:
        print(error)
        print("Starting background thread AGAIN due to error")
        new_selenium_crawl_thread = threading.Thread(target=selenium_crawl_task)
        new_selenium_crawl_thread.setDaemon(True)
        new_selenium_crawl_thread.start()


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
            continue;  # consider break; to stop the loop
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
        print(
            {'link': offer_page_link, 'imageUrl': img_url, 'site_name': site_name, 'primaryCategory': primary_category,
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
            continue;  # consider break; to stop the loop
        try:
            img_url = row.find("div", attrs={"class": "imageContainer"}).img.attrs.get("data-original", "")
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
    site_name = "thekrazycouponlady.com"
    deal_site = DealSite.objects.get(site_name=site_name)
    print('Crawling thekrazycouponlady.com data and creating links in database ..')
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if CHROMEDRIVER_PATH == '/app/.chromedriver/bin/chromedriver':
            options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", "chromedriver")
            driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        else:
            driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

        driver.implicitly_wait(20)
        driver.get(deal_site.primary_crawl_url)


        try:
            driver.find_element_by_css_selector('.kcl-btn-gray').click()
        except Exception as error:
            print("error .kcl-btn-gray: " + str(error))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element_by_css_selector('.btn-load-more').click()
        except Exception as error:
            print("error .btn-load-more: " + str(error))
        html = driver.page_source
        # print(html)

        bs = BeautifulSoup(html, 'html.parser')

        rows = bs.find_all('div', attrs={"class": "card-default"})
        for row in rows:
            offer_id = row.find("div", attrs={"class": "card-title"}).text
            print(str(offer_id))
            if DealLink.objects.filter(site=deal_site, offer_id=offer_id).count() > 0:
                print("Not a new deal")
                continue;  # consider break; to stop the loop

            title = offer_id
            try:
                img_url = row.find("a", attrs={"class": "card-anchor"}).div.attrs.get("style", "") \
                    .replace("background-image: url(\"", "", 1).replace("\");", "", 1)
                if "hour" not in row.find("span", attrs={"class": "meta-date"}).text:
                    print("Old deal: " + offer_id)
                    continue
            except Exception as error:
                print("error: " + str(error))
                continue
            offer_page_link = row.find("a", attrs={"class": "card-anchor"}).attrs.get("href", "")

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
    finally:
        print("Closing chromedriver")
        driver.quit()
    return


def crawl_hip2save():
    return


def do_simple_crawl():
    crawl_dealnews()
    time.sleep(20)
    crawl_slickdeals()
    time.sleep(20)
    crawl_hip2save()
    time.sleep(20)
    return


def do_selenium_crawl():
    crawl_krazy_coupon_lady()
    time.sleep(900)  # 15 min
    return
