#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler


class EventoHandler(BaseHandler):

    def get(self):
        self.response.write('Handler evento')
