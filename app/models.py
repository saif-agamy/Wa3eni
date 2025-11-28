from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    img_url = db.Column(db.String(100), nullable=True, default="img/users_imgs/default.png")
    about = db.Column(db.String(500), nullable=True, default="Edit your profile to type About section.")
    posts_num = db.Column(db.Integer, nullable=True, default=0)
    from_GAN_school = db.Column(db.Boolean, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(5000),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(MutableList.as_mutable(db.JSON), nullable=True)
    upvotes = db.Column(db.Integer, nullable=False)

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete='CASCADE'))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)