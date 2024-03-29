from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    pass


class QuestionSchema(Schema):
    pass


class ThemeListSchema(Schema):
    pass


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    pass
