from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)

class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema), required=True)

class ThemeAddRequestSchema(Schema):
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)

class AnswerRequestSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)
    

class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True)

class QuestionListSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema), required=True)

class QuestionAddRequestSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerRequestSchema), required=True)

class QuestionListQuerystringSchema(Schema):
    theme_id = fields.Int(required=False)
