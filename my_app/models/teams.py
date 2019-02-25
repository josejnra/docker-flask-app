from datetime import datetime

from models.players import PlayersModel
from my_app.app import db


class TeamsModel(db.Model):
    __tablename__ = 'teams'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name              = db.Column(db.String(255), nullable=False)
    city              = db.Column(db.String(255), nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    players = db.relationship(PlayersModel)
