#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
import util.json

class UsuarioHandler(BaseHandler):

    def get(self):
        self.response.write(util.json.to_json({'True': False}))
