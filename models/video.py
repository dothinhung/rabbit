from mongoengine import *

class Video(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()
    duration = IntField()

class Cardio(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()
    duration = IntField()

