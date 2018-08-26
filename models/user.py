from mongoengine import *

class User(Document):
    fname = StringField()
    email = EmailField()
    uname = StringField()
    password = StringField()
