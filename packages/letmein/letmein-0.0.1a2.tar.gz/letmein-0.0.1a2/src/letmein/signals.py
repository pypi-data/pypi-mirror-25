# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals
from django.dispatch import Signal

user_logged_in = \
    Signal(providing_args=['request', 'user'])

user_login_failed = \
    Signal(providing_args=['credentials'])

user_logged_out = \
    Signal(providing_args=['request', 'user'])