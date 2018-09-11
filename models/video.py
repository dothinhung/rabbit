from mongoengine import *

class Video(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()
    duration = IntField()

class Underweight(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()

class Yoga(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()

class Cardio(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()

class Exercise(Document):
    title = StringField()
    link = StringField()
    thumbnail = StringField()
    youtube_id = StringField()
