from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Int(required=False)
    # it's worth to use fields.Email
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminLoginRequestSchema(Schema):
    # it's worth to use fields.Email 
    # but it would distinguish invalid and unknown emails
    email = fields.Str(description="email", required=True)
    password = fields.Str(description="password", required=True)


class AdminLoginResponseSchema(Schema):
    id = fields.Int()
    # it's worth to use fields.Email
    email = fields.Str()
