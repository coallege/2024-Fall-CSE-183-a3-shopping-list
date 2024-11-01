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
        set_check = URL('set_check'),
        remove_url = URL('remove'),
        # Add other things here.
    )

@action('load_data')
@action.uses(db, auth.user, session)
def load_data():
    products = []
    for row in db(db.shopping_list.user_id == auth.user_id).select():
        products.append({
            "id": row.id,
            "product_name": row.product_name,
            "checked": row.checked,
        })
    return products

@action('add')
@action.uses(db, auth.user, session)
def add():
    db.shopping_list.insert(
        product_name=request.params.get("product_name"),
        checked=False,
        user_id=auth.user_id,
    )

@action('set_check')
@action.uses(db, auth.user, session)
def czech():
    db(db.shopping_list.id == int(request.params.get("id"))).update(
        checked=bool(request.params.get("checked"))
    )

@action('remove')
@action.uses(db, auth.user, session)
def remove():
    db(db.shopping_list.id == int(request.params.get("id"))).delete()

# @action('add', method=["GET", "POST"])
# @action.uses('add.html', db, auth.user)
# def add():
#     if request.method == "GET":
#         return dict()
#     else:
#         # This is a form submission.
#         print("User:", get_user_email(), "Product:", request.params.get("product_name"))
#         # Insert product
#         db.product.insert(product_name=request.params.get("product_name"))
#         redirect(URL('add')) # We always redirect after successful form processing.

# # You can add other controllers here.
