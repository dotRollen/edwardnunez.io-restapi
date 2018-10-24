from random import randint
import sys
from faker import Faker
from . import db
from .models.auth import User


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 confirmed=True,
                 member_since=fake.past_date())
        u.pasword = 'password'
        try:
            u.save()
            i += 1
        except:
            e = sys.exc_info()[0]
            print("<p>Error: %s</p>" % e)
