#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path
from uuid import uuid4
import json

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class ShoppingCart(object):
    def __init__(self):
        self._total_inventory = 10
        self._callbacks = []
        self._carts = {}

    def register(self, callback):
        self._callbacks.append(callback)

    def unregister(self, callback):
        self._callbacks.remove(callback)

    def move_item_to_cart(self, session):
        if session in self._carts:
            return
        self._carts[session] = True
        self.notify_callbacks()

    def remove_item_from_cart(self, session):
        if session not in self._carts:
            return
        del self._carts[session]
        self.notify_callbacks()

    def notify_callbacks(self):
        for callback in self._callbacks:
            callback(self.get_inventory_count())

    def get_inventory_count(self):
        return self._total_inventory - len(self._carts)


class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shopping_cart.get_inventory_count()
        self.render('index_sockets.html', session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')
        if session is None:
            self.set_status(400)
            return
        if action == 'add':
            self.application.shopping_cart.move_item_to_cart(session)
        elif action == 'remove':
            self.application.shopping_cart.remove_item_from_cart(session)
        else:
            self.set_status(400)

class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.shopping_cart.register(self._callback)

    def _callback(self, count):
        self.write_message(json.dumps(dict(inventory_count=count)))

    def on_close(self):
        self.application.shopping_cart.unregister(self._callback)

    def on_message(self, message):
        pass

class Application(tornado.web.Application):
    def __init__(self):
        self.shopping_cart = ShoppingCart()
        handlers = [
            (r'^/', DetailHandler),
            (r'^/cart/', CartHandler),
            (r'^/cart/status/', StatusHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
