# coding: utf-8

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup as Soup
from abc import ABCMeta, abstractmethod
from urlparse import urlparse, parse_qs

from items import ReviewItem


class Spider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, html):
        return None

    @abstractmethod
    def crawl(self, page=0):
        return None


class GoogleSpider(Spider):
    '''
    >>> id = 'com.google.android.youtube'
    >>> reviews = GoogleSpider(id).crawl()
    >>> rating = reviews[0].rating
    >>> rating_range = range(1, 6)
    >>> assert rating in rating_range
    '''

    def __init__(self, id, service='google', headers={}):
        super(GoogleSpider, self).__init__()

        self.id = id
        self.service = service
        self.url = 'https://play.google.com/store/getreviews?authuser=0'
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'user-agent': 'Mozilla/5.0'
        }.update(headers)

    def parse(self, html):
        '''parse html and returns Review objects list'''
        soup = Soup(html)
        items = soup.select('.single-review')
        reviews = []
        for item in items:
            review = ReviewItem()

            review.service = self.service

            # user_id
            review.user_id = parse_qs(
                urlparse(item.select('a')[0]['href']).query
            )['id'][0].encode('utf-8')

            item.select('.review-link')[0].extract()

            # username
            username = item.select('.author-name a')
            if username:
                review.username = username[0].text.encode('utf-8')
            else:
                review.username = ''

            # text
            review.text = item.select('.review-body')[0].text.encode('utf-8')

            # rating
            style = item.select('.current-rating')[0]['style']
            review.rating = int(
                style.split(':')[1].strip().replace(';', '').replace('%', '')
            ) / 20

            # review_date
            review_date = item.select('.review-date')[0].text.split()
            d = datetime(*[int(el[:-1]) for el in review_date])
            review.create_date = int(d.strftime('%Y%m%d%H%M%S'))

            reviews.append(review)

        return reviews

    def crawl(self, page=0, hl='ko'):
        payload = {
            'id': self.id,
            'reviewType': 0,
            'pageNum': page,
            'reviewSortOrder': 0,
            'xhr': 1,
            'hl': hl
        }
        r = requests.post(self.url, data=payload, headers=self.headers)
        try:
            content = json.loads(r.content[5:])[0]
        except ValueError:  # sometimes google send awkard response to test bot
            return None
        return self.parse(content[2]) if content and 3 < len(content) else None


if '__main__' == __name__:
    id = 'com.google.android.youtube'
    for review in GoogleSpider(id).crawl(0):
        print review.create_date, review.text, review.rating
