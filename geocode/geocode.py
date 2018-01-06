# -*- coding: utf-8 -*-

import urllib
import urllib2
import util.json
from tokens import google_api_key
from google.appengine.ext.ndb import GeoPt

API_URL = u'https://maps.googleapis.com/maps/api/geocode/json?'
API_KEY = google_api_key


def encontrar_coordenadas(direccion):
    param = {'address': direccion.encode('utf-8'), 'key': API_KEY}
    req = urllib2.Request(API_URL+urllib.urlencode(param))
    res = urllib2.urlopen(req)
    res_json = res.read()
    res.close()
    parsed = util.json.from_json(res_json)
    if parsed.get('results'):
        location = parsed['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return GeoPt(lat,lng)
    else:
        return None