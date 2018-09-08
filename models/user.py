from mongoengine import *
import mlab

mlab.connect

class Body(Document):
    height = IntField()
    weight = IntField()
    time = DateTimeField()
    bmi = FloatField()
    bmi_type = StringField()
<<<<<<< HEAD
=======

class User(Document):
    fname = StringField()
    email = EmailField()
    uname = StringField()
    password = StringField()
    bmi_id = ListField(ReferenceField(Body))


>>>>>>> 93ba622f72a6fadd30ad6f18a0df7cb8a7295d67

class User(Document):
    fname = StringField()
    email = EmailField()
    uname = StringField()
    password = StringField()
    bmi_id = ListField(ReferenceField(Body))