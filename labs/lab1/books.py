#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'books.html',
            title='Home Page',
            header='Books that are great',
            books=[
            'Learning Python',
            'Programming Collective Intelligence',
            'Restful Web Services',
            ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r'^/', BookHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
