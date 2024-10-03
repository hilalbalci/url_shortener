from marshmallow import Schema, fields


class AccountSchema(Schema):
    name = fields.String(required=True)
    daily_limit = fields.Integer(required=True)


class UrlSchema(Schema):
    url = fields.Url(required=True)
