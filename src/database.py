from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# Users Table
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email=db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())

  def __repr__(self) -> str:
    return f'User ||  {self.username}'

