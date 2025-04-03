import datetime as dt

from marshmallow import Schema, fields, validate

class Book(object):
    def __init__(self, id, title, author):
        self.title = title
        self.id = id
        self.author = author

    def __repr__(self):
        return '<Book(name={self.title!r})>'.format(self=self)
    
class BookSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    author = fields.Str(required=True, validate=validate.Length(min=1))
    type = fields.Str(required=True, validate=validate.Length(min=1))