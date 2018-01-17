# -*- coding: utf-8 -*-
""" Private API for Flickr API """

import urllib
import urllib2
import collections
import util.json

from google.appengine.api import memcache

from tokens import flickr_api_key

API_URL = u'https://api.flickr.com/services/rest/'
API_KEY = flickr_api_key
MINUTES_CACHE_DURATION = 30


def do_request(method, params):
    params = dict(params)
    params.update({ u'api_key': API_KEY, u'format': u'json', 'method': method })
    url = build_url(params)

    memcache_value = memcache.get(u'flickr:{}'.format(url))
    if memcache_value:
        return util.json.from_json(memcache_value)

    req = urllib2.Request(API_URL + url)
    req.add_header('User-Agent', 'pyckr-melchor9000')
    res = urllib2.urlopen(req)
    res_json = res.read()
    res.close()
    res_json = res_json[14:-1]
    parsed = util.json.from_json(res_json)
    memcache.set(u'flickr:{}'.format(url), res_json, time=MINUTES_CACHE_DURATION*60)
    return parsed


def build_url(params):
    params = collections.OrderedDict(sorted(params.iteritems()))
    return u'?' + urllib.urlencode(params)


class Photo(object):
    def __init__(self, obj):
        super(Photo, self).__init__()
        self.id = obj[u'primary'] if u'primary' in obj else obj[u'id']
        secret = obj[u'secret']
        server = obj[u'server']
        farm = obj[u'farm']
        self.title = obj[u'title'] if isinstance(obj[u'title'], (unicode, str)) else None
        self.thumbnail_url = u"https://farm%s.staticflickr.com/%s/%s_%s_q.jpg" % (farm, server, self.id, secret)
        self.medium_size_url = u"https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (farm, server, self.id, secret)
        self.kind_large_size_url = u"https://farm%s.staticflickr.com/%s/%s_%s_b.jpg" % (farm, server, self.id, secret)


class PhotoSetPhotos(object):
    def __init__(self, obj):
        super(PhotoSetPhotos, self).__init__()
        self.id = obj[u'id']
        primary_id = obj[u'primary']
        self.owner = obj[u'owner']
        self.ownername = obj[u'ownername']
        self.photos = [ Photo(photo_obj) for photo_obj in obj[u'photo'] ]
        self.primary = [ x for x in self.photos if x.id == primary_id ][0]


class PhotoSetInfo(object):
    def __init__(self, obj):
        super(PhotoSetInfo, self).__init__()
        self.id = obj[u'id']
        self.primary = Photo(obj)
        self.owner = obj[u'owner']
        self.username = obj[u'username']
        self.photos = obj[u'photos']
        self.title = obj[u'title'][u'_content']
        self.description = obj[u'description'][u'_content']
