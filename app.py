# -*- coding: utf-8 -*-

"""
File: app.py
Author: timfeirg
Email: liuyifu@ricebook.com
Github: https://github.com/timfeirg/
Description: navipath tornado app
"""

import motor
import tornado
import tornado.web


class POIHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, world')

    def post(self):
        """
        * `user_id` (mongo object id, optional) - user id
        * `location` (geojson feature, point) - geojson feature, with all interested properties
        * `poi_id` (mongo object id) - generated the same way as `place_id`
        * `name` (string) - name of the point
        * `tag` (list of string, optional) - feature of the poi
        """
        poi_id = self.get_argument('poi_id')
        poi_file = self.get_argument('poi_file')
        user_id = self.get_argument('user_id', None)
        user_id = self.get_argument('user_id', None)
        doc = {'poi': }
        self.settings['db']['poi'].insert(doc, callback=insert_callback)
        responson = {'status': 'OK'}
        self.write(responson)


def insert_callback(result, error):
    print(repr(result))


class PathHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')

    @tornado.web.asynchronous
    def post(self):
        """
        * `user_id` (mongo object id) - user id
        * `from`, `to` (`poi` clause) - the `poi` of the start and destination
        * `path` - (geojson linestring) - the actual path that's collected from
        the user
        """
        # departure_id = self.get_argument('departure_id')
        # destination_id = self.get_argument('destination_id')
        # path_file = self.get_argument('path_file')
        # user_id = self.get_argument('user_id', None)

mongo_client = motor.MotorClient('mongodb://localhost:27017')
navipath_db = mongo_client['navipath']
navipath_app = tornado.web.Application(
    [
        (r'/path.json', PathHandler),
        (r'/poi.json', POIHandler),
    ],
    db=navipath_db,
    debug=True,
)


if __name__ == '__main__':
    navipath_app.listen(8888, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
