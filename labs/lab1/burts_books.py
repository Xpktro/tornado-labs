#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'^/', MainHandler),
            (r'^/recommended/', RecommendedHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={'Book': BookModule},
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)

#   def embedded_javascript(self):
#       return u'document.write(\'hi!\');'

#   def embedded_css(self):
#       return u'.book {background-color: red !important;}'

#   def html_body(self):
#       return u'<script>document.write(\'Hello!\');</script>'

    def css_files(self):
        return u'/static/css/newreleases.css'

    def javascript_files(self):
        return u'https://ajax.googleapis.com/ajax/libs/jqueryui/' \
            u'1.8.14/jquery-ui.min.js'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'burt-index.html',
            page_title='Burt\'s Books | Home',
            header_text='Welcome to Burt\' Books!',
        )


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('recommended.html',
            page_title='Burt\'s Books | Recommended Reading',
            header_text='Recommended Reading',
            books=[
            {
            'title': 'Programming Collective Intelligence',
            'subtitle': 'Building Smart Web 2.0 Applications',
            'image':'/static/images/collective_intelligence.gif',
            'author': 'Toby Segaran',
            'date_added': 1310248056,
            'date_released': 'August 2007',
            'isbn': '978-0-596-52932-1',
            'description': '''
            <p>This fascinating book demonstrates how you can build web 
            applications to mine the enormous amount of data created by
            people on the Internet. With the sophisticated algorithms in
            this book, you can write smart programs to access interesting
            datasets from other web sites, collect data from users of your
            own applications, and analyze and understand the data once
            you've found it.</p>
            '''
            },] * 10)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
