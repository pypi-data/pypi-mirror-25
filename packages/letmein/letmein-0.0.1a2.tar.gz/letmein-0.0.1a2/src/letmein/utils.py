# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import hashlib

import os
from django.conf import settings


def generate_password():
    hash_algorithm = getattr(
        settings,
        'USERPASSWORD_HASH_ALGORITHM',
        'sha256')

    hash_algo = getattr(hashlib, hash_algorithm)

    m1 = hash_algo()
    m1.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
    m1.update(os.urandom(16))

    m2 = hash_algo()
    m2.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
    m2.update(os.urandom(16))

    m3 = hash_algo()
    m3.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
    m3.update(os.urandom(16))

    if getattr(settings, 'USERCODE_NUMERIC_CODES', False):
        hashed = (
            str(int(m1.hexdigest(), 16))[-60:] +
            str(int(m2.hexdigest(), 16))[-60:] +
            str(int(m3.hexdigest(), 16))[-60:]
        )
    else:
        hashed = (
            m1.hexdigest()[:60] +
            m2.hexdigest()[:60] +
            m3.hexdigest()[:60]
        )

    return hashed