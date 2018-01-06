#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
import webapp2
import tokens


class CategoriaHandler(BaseHandler):

    def get(self):
        self.response.write('Handler categoria')
