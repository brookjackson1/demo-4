import os
from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-development')

# Register Blueprints
from app.blueprints.countries import countries
from app.blueprints.cities import cities

app.register_blueprint(countries, url_prefix='/countries')
app.register_blueprint(cities, url_prefix='/cities')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)