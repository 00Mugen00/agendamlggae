# -*- coding: utf-8 -*-
""" URLs API of Flickr """
import flickr.api


def lookup_user(url):
    """ Given an flickr url, returns the user id for that. Only valid if the url doesn't
    contain the user id. FE.: <code>http://www.flickr.com/photos/metropolis462/</code> will return
    <code>133842466@N08</code>."""
    res = flickr.api.do_request(
        u'flickr.urls.lookupUser',
        { u'url': url }
    )
    return res[u'user'][u'id'] if u'user' in res else None
