from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sayhi'

db = SQLAlchemy(app)
app.app_context().push()

admin = Admin(app,template_mode='bootstrap3')

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True)
  password = db.Column(db.String)
  age = db.Column(db.Integer)
  birthday = db.Column(db.DateTime)

  comments = db.relationship('Comment', backref='User', lazy='dynamic')

  def __repr__(self):
    return f'<User {self.username}>'
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.String(200))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f'<Comment {self.comment}>'

class CommentView(ModelView):
    form_columns = [
        'comment',
        'user_id',
    ]
    list_columns = [
        'comment',
        'user_id',
    ]

admin.add_view(ModelView(User,db.session))
admin.add_view(CommentView(Comment,db.session))

if __name__ == '__main__':
    app.run(debug=True)