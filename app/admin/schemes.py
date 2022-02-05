from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminLoginRequestSchema(Schema):
    email = fields.Str(description='email', required=True)
    password = fields.Str(description='password', required=True)


class AdminLoginResponseSchema(Schema):
    id = fields.Int()
    email = fields.Str()
