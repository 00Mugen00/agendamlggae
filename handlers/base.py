#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2


class BaseHandler(webapp2.RequestHandler):
    """Handler Base para el resto de handlers"""
    def dispatch(self):
        """Añadir a todas las respuesta el header field de content type adecuado"""
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        super(BaseHandler, self).dispatch()
