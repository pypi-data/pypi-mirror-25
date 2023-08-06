# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import NoResultFound
from htmlclientdejavu.backends.base import SessionBase
from htmlclientdejavu.backends.base import CreateError
from htmlclientdejavu.backends.base import UpdateError
from htmlclientdejavu.settings import dejavu_settings

from modelchemy import dbs


class SessionStore(SessionBase):
    _entity = None
    _table = None
    _request_session = None

    @property
    def Session(self):
        return self.modelchemy.Session()

    @property
    def Entity(self):
        return dejavu_settings.MODEL

    @property
    def Table(self):
        return dejavu_settings.TABLE

    def exists(self, session_key):
        db_session = self.Session

        q = (
            db_session.query(self.Entity).
                filter(self.Table.c.session_key == session_key)
        )

        count = q.count()

        if count == 1:
            return True
        elif count == 0:
            return False

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()

            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return

    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        return self.Entity(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=(
                self.get_expiry_date().
                    astimezone(timezone.utc).replace(tzinfo=None)
            ),
        )

    def save(self, must_create=False):
        """
        Saves the session data. If 'must_create' is True, a new session object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() only updates an existing object and does not create one
        (an UpdateError is raised).
        """

        db_session = self.Session

        if self.session_key is None:
            return self.create()

        data = self._get_session(no_load=must_create)
        obj = self.create_model_instance(data)

        db_session.merge(obj)

        try:
            db_session.commit()
        except IntegrityError:
            if must_create:
                raise CreateError
            raise
        except DatabaseError:
            if not must_create:
                raise UpdateError
            raise

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key

        db_session = self.Session

        db_session.execute(
            self.Table.delete().
                where(self.Table.c.session_key == session_key)
        )

        db_session.commit()

    def load(self):
        db_session = self.Session

        q1 = (
            db_session.query(self.Entity).
                filter(self.Table.c.session_key == self.session_key).
                filter(self.Table.c.expire_date >
                       (timezone.now().astimezone(timezone.utc).
                        replace(tzinfo=None))
                       )
        )

        try:
            s = q1.one()
        except NoResultFound:
            self._session_key = None
            return {}

        return self.decode(s.session_data)

    @classmethod
    def clear_expired(cls):

        t_cookie_sessions = dbs.router.retrieve(
            dejavu_settings.MODEL).default()

        db_session = dbs.Session()

        db_session.execute(
            t_cookie_sessions.delete().
                where(t_cookie_sessions.c.expire_date <
                      (timezone.now().astimezone(timezone.utc).
                       replace(tzinfo=None))
                      )
        )

        db_session.commit()
        db_session.close()
