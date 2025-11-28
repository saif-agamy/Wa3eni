from app import app, db
from models import Post,User,Upvote

# Run inside app context
with app.app_context():
    Post.__table__.drop(db.engine)
    Post.__table__.create(db.engine)

    Upvote.__table__.drop(db.engine)
    Upvote.__table__.create(db.engine)

    # User.__table__.drop(db.engine)
    # User.__table__.create(db.engine)
    print("done")
