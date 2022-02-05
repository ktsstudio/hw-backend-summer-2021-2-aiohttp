from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)

class ThemeAddRequestSchema(Schema):
    title = fields.Str(required=True)
    
class ThemeAddResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()


class QuestionSchema(Schema):
    pass


class AnswerSchema(Schema):
    pass


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(lambda: ThemeSchema()), required=True)


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    pass
