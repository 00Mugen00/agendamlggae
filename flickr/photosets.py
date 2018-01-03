# -*- coding: utf-8 -*-
""" PhotoSets API of Flickr """
import flickr.api


def get_photos(user_id, photoset_id):
    """ Given an user_id and a photoset_id, returns the PhotoSetPhotos object for that
    request"""
    res = flickr.api.do_request(
        u'flickr.photosets.getPhotos',
        { u'user_id': user_id, u'photoset_id': photoset_id }
    )
    return flickr.api.PhotoSetPhotos(res[u'photoset']) if res[u'photoset'] else None


def get_info(user_id, photoset_id):
    """ Given an user_id and a photoset_id, returns the PhotoSetInfo object for that
    request"""
    res = flickr.api.do_request(
        u'flickr.photosets.getInfo',
        { u'user_id': user_id, u'photoset_id': photoset_id }
    )
    return flickr.api.PhotoSetInfo(res[u'photoset']) if res[u'photoset'] else None
