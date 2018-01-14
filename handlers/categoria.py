#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler


class CategoriaHandler(BaseHandler):

    def get(self):
        self.response.write('Handler categoria')
