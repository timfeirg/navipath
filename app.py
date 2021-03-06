"""
File: app.py
Author: timfeirg
Email: liuyifu@ricebook.com
Github: https://github.com/timfeirg/
Description: navipath tornado app
"""

import motor
import os
import json
import tornado
import tornado.web

# not NotImplemented
import olc


EARTH_RADIUS = 6378.1  # kilometers


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class POIHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        """
        * `location` (OLC or list) - user location, could be represented with
        OLC location or latitude & longitude
        * `user_id` (mongo object id, optional) - user who initiate this query
        * `filter` (string, optional) - dict that contains custom search
        parameter, should provide tags or creator, and filter results
        corresponndingly
        """
        db_poi = self.settings['db'].poi
        cursor = db_poi.find({}, {'name': 1, '_id': 0})
        poi_list = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            poi_list.append(doc)

        response = {
            'status': 0,
            'result': poi_list,
        }
        self.write(response)

    def post(self):
        """
        create POI
        * `user_id` (mongo object id, optional) - user id
        * `location` (list of float) - [longitude, latitude]
        * `poi_tag` (list of string, optional) - feature of the poi
        """
        raise NotImplemented
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

    @tornado.gen.coroutine
    def get(self):
        db_path = self.settings['db'].path
        cursor = db_path.find({}, {'_id': 0})
        path_list = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            path_list.append(doc)

        response = {
            'status': 0,
            'result': path_list,
        }
        self.write(response)

    @tornado.gen.coroutine
    def post(self):
        """
        * `user_id` (mongo object id) - user id
        * `from`, `to` (list of float) - poi_id of the starting point and destination
        * `path` - (list of coordinates) - the actual path that's collected from the user
        """
        fromm = self.get_argument('from')
        too = self.get_argument('to')
        raw_path = json.loads(self.get_argument('path'))
        path = [[float(x), float(y)] for [x, y] in raw_path]
        doc = {
            'from': fromm,
            'to': too,
            'path': path,
        }

        self.settings['db']['path'].insert(doc, callback=insert_callback)


root = os.path.dirname(__file__)
port = 8888

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR))

mongo_client = motor.MotorClient('mongodb://localhost:27017')
navipath_db = mongo_client['navipath']
navipath_app = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r'/asset/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_ROOT + '/asset'}),
        (r'/path.json', PathHandler),
        (r'/poi.json', POIHandler),
    ],
    db=navipath_db,
    debug=True,
    template_path=root,
    static_path=root
)


def insert_callback(result, error):
    print(repr(result))


def make_poi_id(longitude, latitude):
    long_str = round(longitude, 12)
    lat_str = round(latitude, 12)
    obj_id = long_str + lat_str
    return obj_id


if __name__ == '__main__':
    navipath_app.listen(port, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
