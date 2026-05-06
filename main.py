from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

    comments = db.relationship('Comment', backref='post')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    replies = db.relationship('Comment')

with app.app_context():
    db.create_all()

    post = Post(title="First Post")

    c1 = Comment(text="Great!", post=post)
    c2 = Comment(text="Reply to great", post=post, parent_id=1)

    db.session.add_all([post, c1, c2])
    db.session.commit()

    comments = Comment.query.all()
    for c in comments:
        print(c.text)
