#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Henlo friend. I see u come h3re but there\'s no API yet :(')


app = webapp2.WSGIApplication([
    ('/agendamlg-api/', MainHandler)
], debug=True)
