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
        """
        * `user_id` (mongo object id, optional) - user id
        * `query` (string, optional) - custom search parameter, if provided,
        will be searched against all tags in nearby places, if empty, recommend
        poi based on distance
        """
        self.write('Hello, world')

    def post(self):
        """
        * `user_id` (mongo object id, optional) - user id
        * `location` (geojson feature, point) - geojson feature, with all
        interested properties
        * `poi_tag` (list of string, optional) - feature of the poi
        """
        user_id = self.get_argument('user_id', None)
        location = self.get_argument('location')
        poi_tag = self.get_argument('poi_tag', None)

        doc = {
            'location': location,
            'poi_id': make_poi_id(**location['features'])
        }
        if user_id:
            doc.update({'user_id': user_id})

        if poi_tag:
            doc.update({'poi_tag': poi_tag})

        self.settings['db']['poi'].insert(doc, callback=insert_callback)
        responson = {'status': 'OK'}
        self.write(responson)


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
        pass

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

def insert_callback(result, error):
    print(repr(result))


def make_poi_id(longitude, latitude):
    long_str = round(longitude, 12)
    lat_str = round(latitude, 12)
    obj_id = long_str + lat_str
    return obj_id


if __name__ == '__main__':
    navipath_app.listen(8888, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
