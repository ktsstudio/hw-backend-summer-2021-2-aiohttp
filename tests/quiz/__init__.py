from app.quiz.models import Answer, Question, Theme


def theme2dict(theme: Theme):
    return {
        "id": int(theme.id),
        "title": str(theme.title),
    }


def question2dict(question: Question):
    return {
        "id": int(question.id),
        "title": str(question.title),
        "theme_id": int(question.theme_id),
        "answers": [answer2dict(answer) for answer in question.answers],
    }


def answer2dict(answer: Answer):
    return {
        "title": answer.title,
        "is_correct": answer.is_correct,
    }
