from datetime import datetime
from .. import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_email = db.Column(db.String(256), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    file_name = db.Column(db.String())
    description = db.Column(db.Text)
    size = db.Column(db.Integer)
    hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<File {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return File.query.all()

    @staticmethod
    def get_by_id(id):
        return File.query.get(id)

    @staticmethod
    def get_by_hash(hash):
        return File.query.filter_by(hash=hash).first()

    @staticmethod
    def get_by_user(user_id):
        return File.query.filter_by(user_id=user_id).all()