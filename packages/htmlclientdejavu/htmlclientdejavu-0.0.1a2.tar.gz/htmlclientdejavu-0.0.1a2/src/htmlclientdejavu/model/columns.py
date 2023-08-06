# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from sqlalchemy import Column, String, Text, DateTime

session_key_column = Column(
    'session_key',
    String(40),
    primary_key=True
)

session_data_column = Column(
    'session_data',
    Text(),
)

session_expire_date_column = Column(
    'expire_date',
    DateTime(),
    index=True,
)

SessionKeyColumn = lambda: session_key_column.copy()
SessionDataColumn = lambda: session_data_column.copy()
SessionExpireDateColumn = lambda: session_expire_date_column.copy()
