from quiz import app, db
from quiz.models import User, QuestionTopics, QuestionDifficulties

def init_db():
    with app.app_context():
        if len(User.query.all()) == 0: # Checks if any users exist
            db.drop_all() # Deletes old table and makes new one
            db.create_all()
            created_user = User(username="user1", email="user1@email.com", password="123456") # Adds a user to table
            db.session.add(created_user)
            db.session.commit()
            # Adds record for number of questions answered for each difficulty and topic for new user
            question_topics = QuestionTopics(user_id=created_user.id)
            question_difficulties = QuestionDifficulties(user_id=created_user.id)
            db.session.add(question_topics)
            db.session.add(question_difficulties)
            db.session.commit()

if __name__ == "__main__":
    init_db() # Creates new tables if no records are present
    print(app.url_map)
    app.run(debug=True)
