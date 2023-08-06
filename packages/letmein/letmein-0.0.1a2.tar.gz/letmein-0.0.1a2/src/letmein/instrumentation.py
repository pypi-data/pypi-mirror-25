# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import weakref

import six
from sqlalchemy import types
from sqlalchemy.ext.mutable import Mutable
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class ScalarCoercible(object):
    def _coerce(self, value):
        raise NotImplemented

    def coercion_listener(self, target, value, oldvalue, initiator):
        return self._coerce(value)


class DjangoPassword(Mutable, object):
    @classmethod
    def coerce(cls, key, value):

        if isinstance(value, DjangoPassword):
            return value

        if isinstance(value, (six.string_types)):
            return cls(value)

        super(DjangoPassword, cls).coerce(key, value)

    def __init__(self, value, context=None, secret=False):
        # Store the hash (if it is one).
        self.hash = value if not secret else None

        # Store the secret if we have one.
        self.secret = value if secret else None

        # The hash should be bytes.
        if isinstance(self.hash, six.text_type):
            self.hash = self.hash.encode('utf8')

        # Save weakref of the password context (if we have one)
        self.context = weakref.proxy(context) if context is not None else None

    def __eq__(self, value):

        if self.hash is None or value is None:
            # Ensure that we don't continue comparison if one of us is None.
            return self.hash is value

        if isinstance(value, DjangoPassword):
            # Comparing 2 hashes isn't very useful; but this equality
            # method breaks otherwise.
            return value.hash == self.hash

        if self.context is None:
            # Compare 2 hashes again as we don't know how to validate.
            return value == self

        if isinstance(value, (six.string_types)):
            return self.context.check_password(value, self.hash)

        return False

    def __ne__(self, value):
        return not (self == value)


class DjangoPasswordContext(object):
    _hasher = 'default'

    def __init__(self, **kwargs):
        self._hasher = kwargs.get('hasher', 'default')

    def encrypt(self, value):
        return make_password(value, hasher=self._hasher)

    def check_password(self, value, hash):
        return check_password(value, hash, None, preferred=self._hasher)


class DjangoPasswordType(types.TypeDecorator, ScalarCoercible):

    impl = types.VARCHAR(128)
    python_type = DjangoPassword

    def __init__(self, max_length=None, **kwargs):

        self.context = DjangoPasswordContext(**kwargs)

        self._max_length = max_length

        self.impl = types.VARCHAR(self.length)

    @property
    def length(self):
        """Get column length."""
        if self._max_length is None:
            self._max_length = self.calculate_max_length()

        return self._max_length

    def calculate_max_length(self):
        return 128

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(self.length))

    def process_bind_param(self, value, dialect):
        if isinstance(value, DjangoPassword):
            # If were given a password secret; encrypt it.
            if value.secret is not None:
                return self.context.encrypt(value.secret).encode('utf8')

            # Value has already been hashed.
            return value.hash

        if isinstance(value, six.string_types):
            # Assume value has not been hashed.
            return self.context.encrypt(value).encode('utf8')

    def process_result_value(self, value, dialect):
        if value is not None:
            return DjangoPassword(value, self.context)

    def _coerce(self, value):

        if value is None:
            return

        if not isinstance(value, DjangoPassword):
            # Hash the password using the default scheme.
            value = self.context.encrypt(value).encode('utf8')
            return DjangoPassword(value, context=self.context)

        else:
            # If were given a password object; ensure the context is right.
            value.context = weakref.proxy(self.context)

            # If were given a password secret; encrypt it.
            if value.secret is not None:
                value.hash = self.context.encrypt(value.secret).encode('utf8')
                value.secret = None

        return value

    @property
    def python_type(self):
        return self.impl.type.python_type
