from database import db
from datetime import datetime


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


class Note(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    filename = db.Column(
        db.String(300),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=True
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=False
    )


class SavedSummary(db.Model):

     id = db.Column(
        db.Integer,
        primary_key=True
    )

     user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )
     note_id = db.Column(
        db.Integer,
        db.ForeignKey("note.id")
    )

     content = db.Column(
        db.Text,
        nullable=False
    )

     created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
     
class SavedQuiz(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    note_id = db.Column(
        db.Integer,
        db.ForeignKey("note.id")
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class SavedFlashcard(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    note_id = db.Column(
        db.Integer,
        db.ForeignKey("note.id")
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Bookmark(db.Model):

     id = db.Column(
        db.Integer,
        primary_key=True
    )

     user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

     note_id = db.Column(
        db.Integer,
        db.ForeignKey("note.id")
    )
     

class StudyHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    note_id = db.Column(
        db.Integer,
        db.ForeignKey("note.id")
    )

    action = db.Column(
        db.String(50)
    )

    viewed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
     
def __repr__(self):
        return f"<SavedSummary {self.id}>"
