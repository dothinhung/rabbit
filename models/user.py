from mongoengine import *
import mlab

mlab.connect

class User(Document):
    fname = StringField()
    email = EmailField()
    uname = StringField()
    password = StringField()

class Body(Document):
    height = IntField()
    weight = IntField()
    time = DateTimeField()
    bmi = FloatField()
    user_id = ReferenceField(User)
    bmi_type = StringField()

