# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from letmein.instrumentation import DjangoPasswordType

id_user_uuid_col = None
password_passlib_type_col = None

try:
    import sqlalchemy_utils

    from sqlalchemy_utils.types import UUIDType

    id_user_uuid_col = Column(
        'id_user',
        UUIDType(),
        primary_key=True,
        default=uuid.uuid4
    )

except ImportError:
    pass

try:
    import passlib
    import sqlalchemy_utils

    from sqlalchemy_utils.types import PasswordType

    password_passlib_type_col = Column(
        'password',
        PasswordType(
            max_length=200,
            schemes=('pbkdf2_sha512',)
        ),
        nullable=False
    )
except:
    pass

id_user_int_col = Column(
    'id_user',
    Integer,
    primary_key=True,
    nullable=False,
    index=True,
    autoincrement=True,
)

django_password_col = Column(
    'password',
    DjangoPasswordType(),
    nullable=False,
)

username_col = Column(
    'username',
    String(100),
    unique=True,
    nullable=True,
    index=True,
)

is_active_col = Column(
    'is_active',
    Boolean,
    nullable=False,
    default=True
)

is_superuser_col = Column(
    'is_superuser',
    Boolean,
    nullable=False,
    default=False,
)

is_staff_col = Column(
    'is_staff',
    Boolean,
    nullable=False,
    default=False,
)

if id_user_uuid_col is not None:
    IdUserUUIDColumn = lambda : id_user_uuid_col.copy()

if password_passlib_type_col is not None:
    PasswordTypeColumn = lambda : password_passlib_type_col.copy()


IdUserIntColumn = lambda : id_user_int_col.copy()

DjangoPasswordColumn = lambda : django_password_col.copy()

UsernameColumn = lambda : username_col.copy()

IsActiveColumn = lambda : is_active_col.copy()

IsSuperUserColumn = lambda : is_superuser_col.copy()

IsStaffColumn = lambda : is_staff_col.copy()