from . import db


class account(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    apply_money = db.Column(db.Float, index=True)
    autal_money= db.Column(db.Float, index=True)
    note = db.Column(db.String(512), index=True)
    username = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User %r>' % self.username
