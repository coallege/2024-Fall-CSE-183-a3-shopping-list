"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        # For example...
        load_data_url = URL('load_data'),
        add_url = URL('add'),
        set_check_url = URL('set_check'),
        remove_url = URL('remove'),
        # Add other things here.
    )

@action('load_data')
@action.uses(db, auth.user, session)
def load_data():
    products = []
    print(db(db.shopping_list.user_id == auth.user_id).select(orderby=~db.shopping_list.order))
    for row in db(db.shopping_list.user_id == auth.user_id).select(orderby=~db.shopping_list.order):
        products.append({
            "id": row.id,
            "name": row.name,
            "checked": row.checked,
        })
    return products

def order(user_id):
    it = [
        row.order
        for row
        in db(db.shopping_list.user_id == user_id).select(db.shopping_list.order)
        if row.order is not None
    ]
    it.append(0)
    return it

@action('add')
@action.uses(db, auth.user, session)
def add():
    db.shopping_list.insert(
        name=request.params.get("name"),
        checked=False,
        user_id=auth.user_id,
        order=max(order(auth.user_id)) + 1,
    )

@action('set_check')
@action.uses(db, auth.user, session)
def czech():
    this_entry = db(db.shopping_list.id == int(request.params.get("id")))
    print(this_entry)
    if request.params.get("checked") == "true":
        this_entry.update(checked=True, order=min(order(auth.user_id)) - 1)
    else:
        this_entry.update(checked=False, order=max(order(auth.user_id)) + 1)

@action('remove')
@action.uses(db, auth.user, session)
def remove():
    db(
        (db.shopping_list.id == int(request.params.get("id")))
        & (db.shopping_list.user_id == auth.user_id)
    ).delete()
