# coding: utf-8

import os
import sys
import time
import logging

from spiders import GoogleSpider


logging.basicConfig(format='[Crawler]: %(message)s',
                    stream=sys.stdout,
                    level=logging.DEBUG)


class Spy(object):
    def __init__(self, id, name=''):
        self.id = id
        self.name = name
        self.spider = GoogleSpider(id)

    def update_position(self, new_pos=''):
        old_pos = ''
        filename = '%s.pos' % self.id
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                old_pos = fp.readline().strip()

        with open(filename, 'w') as fp:
            fp.write(new_pos)

        return old_pos

    def read(self, page=0):
        '''read content from the given page'''
        return self.spider.crawl(page)

    def plant(self, channel='spy'):
        logging.info('%s spy is back in business.' % self.name)
        reviews = self.read()
        pos = self.update_position(reviews[0].user_id).strip()
        for review in reviews:
            if pos == review.user_id:
                break
            elif 2 >= review.rating:
                rating = ':star:' * review.rating
                username = review.username
                text = review.text
                create_date = str(review.create_date)[:8]

                fmt = '[%s][%s] %s: %s (%s)'
                logging.info(
                    fmt % (self.name, rating, username, text, create_date)
                )
        logging.info('%s spy has returned.' % self.name)


if '__main__' == __name__:
    SLEEP = 60
    youtubeSpy = Spy('com.google.android.youtube', name='Youtube')

    logging.info('Planting Spy...')
    while True:
        youtubeSpy.plant()
        logging.info('%s spy will sleep in %d sec.' % (youtubeSpy.name, SLEEP))
        time.sleep(SLEEP)
