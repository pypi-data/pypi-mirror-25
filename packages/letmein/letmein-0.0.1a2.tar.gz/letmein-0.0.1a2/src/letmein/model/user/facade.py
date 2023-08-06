# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AnonymousUser(object):
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False

    def __init__(self):
        pass

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")



    def has_module_perms(self, lbl):
        return True

    def has_perm(self, lbl):
        return True

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False

    @property
    def is_staff(self):
        return False

    def get_username(self):
        return self.username