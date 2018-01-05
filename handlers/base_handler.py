#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2

# Handler Base para el resto de handlers

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Añadir a todas las respuesta el header field
        # de content type adecuado
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        super(BaseHandler, self).dispatch()