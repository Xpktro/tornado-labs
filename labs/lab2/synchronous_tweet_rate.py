#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import urllib
import json
import datetime
import time
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient

from tornado.options import define, options
define(u'port', default=8000, help=u'run on the given port', type=int)

URL = 'http://pastie.org/pastes/8156731/download?key=pdk4qwzrz1fb5zqwyrwnq'
NOW = datetime.datetime(2012, 9, 21, 22, 51, 28)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        # q=%23freebandnames
        response = client.fetch(URL)
        body = json.loads(response.body)
        result_count = len(body['statuses'])
        now = NOW
        raw_oldest_tweet_at = body['statuses'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
            '%a %b %d %H:%M:%S +0000 %Y')
        seconds_diff = time.mktime(now.timetuple()) - \
            time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.render('tweet-rate.html',
            query='#freebandnames', tweets_per_second=tweets_per_second)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r'^/', IndexHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
