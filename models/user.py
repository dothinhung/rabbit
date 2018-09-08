from mongoengine import *
import mlab

mlab.connect

class Body(Document):
    height = IntField()
    weight = IntField()
    time = DateTimeField()
    bmi = FloatField()
    bmi_type = StringField()

class User(Document):
    fname = StringField()
    email = EmailField()
    uname = StringField()
    password = StringField()
    bmi_id = ListField(ReferenceField(Body))