# -*- coding: utf-8 -*-

"""
File: app.py
Author: timfeirg
Email: liuyifu@ricebook.com
Github: https://github.com/timfeirg/
Description: navipath tornado app
"""

import tornado.ioloop
import tornado.web


class POIHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, world')


class PathHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, world')


navipath_app = tornado.web.Application([
    (r'/path.json', PathHandler),
    (r'/poi.json', POIHandler),
])


if __name__ == '__main__':
    navipath_app.listen(8888, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
