from marshmallow import Schema, fields, post_load
from flaskProject.database import *


class UserData(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class EventData(Schema):
    id = fields.Int()
    name = fields.Str()
    date = fields.DateTime()
    description = fields.Str()
    author = fields.Nested(UserData)

    @post_load
    def create_event(self, data, **kwargs):
        return Event(**data)
