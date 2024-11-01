"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

# should we allow duplicate product names?
# I guess so.
fld_product_name = Field(
    "name",
    type="string",
    requires=IS_NOT_EMPTY()
)

fld_checked = Field(
    "checked",
    type="boolean",
    requires=IS_NOT_EMPTY()
)

fld_order = Field(
    "order",
    type="integer",
    requires=IS_NOT_EMPTY()
)

fkey_user_id = Field(
    "user_id",
    type="integer",
    requires=IS_NOT_EMPTY()
)

# Add here any table definition you need. Below is an example.
db.define_table('shopping_list',
    fld_product_name,
    fld_checked,
    fld_order,
    fkey_user_id,
)

db.commit()
