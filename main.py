import gevent
import json
from bs4 import BeautifulSoup
from urllib2 import urlopen, HTTPError, URLError
from sqlalchemy import text
from flask import request, jsonify
from api import crawl
from models import CrawlerDB
import httplib


def add_acronym_for_page(page, category_id):
    url = u'http://www.acronymslist.com/' + page.attrs['href']
    opened_url = urlopen(url)
    try:
        page = opened_url.read()
    except httplib.IncompleteRead, e:
        page = e.partial
        print "Point 4"
    soup = BeautifulSoup(page, 'html.parser')
    all_acronyms = soup.find_all('a', attrs={'class': 'special'})
    for acronym in all_acronyms:
        name = acronym.contents[0]
        value = acronym.next.next.next
        db = CrawlerDB()
        db.begin()
        try:
            db.insert_row("acronym", **{'category_id': category_id, 'name': name, 'value': value})
            db.commit()
        except Exception as e:
            print e
            db.rollback()


def add_acronym_for_category(category, category_id, threads):
    url = u'http://www.acronymslist.com/' + category.attrs['href']
    opened_url = urlopen(url)
    try:
        page = opened_url.read()
    except httplib.IncompleteRead, e:
        page = e.partial
        print "Point 3"
    soup = BeautifulSoup(page, 'html.parser')
    pages = soup.find_all('a', attrs={'class': 'page'})
    for page in pages:
        threads.append(gevent.spawn(add_acronym_for_page, page, category_id))


def do(url):
    opened_url = urlopen(url)
    try:
        page = opened_url.read()
    except httplib.IncompleteRead, e:
        page = e.partial
        print "Point 2"
    soup = BeautifulSoup(page, 'html.parser')
    all_categories = soup.find_all('a', attrs={'class': None, 'target': None})
    all_categories = all_categories[1:]
    all_categories.pop()
    threads = list()
    for category in all_categories:
        sql = u'select last_insert_id() as id'
        db = CrawlerDB()
        db.begin()
        try:
            db.insert_row("category", **{'name': category.contents[0]})
            result = db.execute_raw_sql(sql, dict())
            category_id = result[0]['id']
            db.commit()
        except Exception as e:
            print e
            print "Point 1"
            db.rollback()
        add_acronym_for_category(category, category_id, threads)
    gevent.joinall(threads)


@crawl.route('/', methods=['POST'])
def crawl_site_and_store_data():
    data = json.loads(request.get_data())
    do(data['url'])
    return jsonify({"success": True})


@crawl.route('/', methods=['GET'])
def check():
    return "true"


if __name__ == "__main__":
    url = 'http://acronymslist.com/'
    do(url)
