from datetime import datetime
from flask import current_app, url_for
from backend.app import db

class Projects(db.Document):
    name = db.StringField()
