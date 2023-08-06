# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from sqlalchemy import MetaData
from sqlalchemy import Table

from htmlclientdejavu.model.columns import SessionDataColumn
from htmlclientdejavu.model.columns import SessionExpireDateColumn
from htmlclientdejavu.model.columns import SessionKeyColumn

t_session_db_storage = Table(
    "session_storage",
    MetaData(),
    SessionKeyColumn(),
    SessionDataColumn(),
    SessionExpireDateColumn(),
)
