# coding: utf-8
from peewee import *


db = MySQLDatabase(
    host='127.0.0.1',
    user='root',
    passwd='qwerasDf2017',
    port=3306,
    database='hotel_comments_2',
    charset='utf8'
)


class BaseModel(Model):
    class Meta:
        database = db


class Urls(BaseModel):
    url_id = PrimaryKeyField()
    url = CharField(max_length=128, unique=True)
    status = CharField(max_length=32, null=False, default='new')

    class Meta:
        db_table = 'urls'


class Hotel(BaseModel):
    hotel_id = CharField(primary_key=True, unique=True, null=False)
    hotel_name = CharField(unique=True, null=False)
    hotel_address = CharField(null=True)

    class Meta:
        db_table = 'hotel'


class Comments(BaseModel):
    comment_id = PrimaryKeyField()
    hotel_id = ForeignKeyField(Hotel, related_name='comments')
    comment = TextField()

    class Meta:
        db_table = 'comments'
