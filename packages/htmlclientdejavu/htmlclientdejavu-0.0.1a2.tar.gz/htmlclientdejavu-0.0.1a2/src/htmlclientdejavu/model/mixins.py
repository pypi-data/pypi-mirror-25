# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

class SessionStorage(object):
    def __init__(self, session_key, session_data, expire_date):
        self.session_key = session_key
        self.session_data = session_data
        self.expire_date = expire_date

    @property
    def get_decoded(self):
        return DatabaseSessionStore().decode(self.session_data)

    @staticmethod
    def encode(session_dict):
        return DatabaseSessionStore().encode(session_dict)

from htmlclientdejavu.backends.db import SessionStore as DatabaseSessionStore