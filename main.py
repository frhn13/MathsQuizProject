from quiz import app, db
from quiz.models import User, QuestionTopics, QuestionDifficulties

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        created_user = User(username="John", email="john@email.com", password="123456")
        db.session.add(created_user)
        db.session.commit()
        question_topics = QuestionTopics(user_id=created_user.id)
        question_difficulties = QuestionDifficulties(user_id=created_user.id)
        db.session.add(question_topics)
        db.session.add(question_difficulties)
        db.session.commit()

if __name__ == "__main__":
    init_db()
    print(app.url_map)
    app.run(debug=True)
