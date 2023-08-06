# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .settings import letmein_settings


class HTMLClientAuthBase(object):
    _entity = None
    _table = None
    _sessionmaker = None

    def get_session(self, request):

        if self._sessionmaker is None:
            self._sessionmaker = request.modelchemy.Session

        return self._sessionmaker

    @property
    def Entity(self):
        return letmein_settings.MODEL

    @property
    def Table(self):
        return letmein_settings.TABLE

    def check_password(self, user, password):
        return (
            user.password == password
        )

    def get_user(self, request, user_id):

        session = self.get_session(request)()

        model = self.Entity
        table = self.Table

        try:
            user = (
                session.query(model).filter(table.c.lid_user == user_id).one()
            )
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

        return user


class UsernameBackend(HTMLClientAuthBase):
    def authenticate(self, request, username=None, password=None):
        session = self.get_session(request)()

        session.expunge_all()
        session.expire_all()

        model = self.Entity
        table = self.Table

        try:
            user = (
                session.query(model).
                    filter(table.c.username == username).
                    one()
            )

            if self.check_password(user, password):
                return user

        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None
