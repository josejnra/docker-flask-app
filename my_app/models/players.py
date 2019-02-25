from datetime import datetime

from models.teams import TeamsModel
from my_app.app import db


class PlayersModel(db.Model):
    __tablename__ = 'players'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name              = db.Column(db.String(255))
    age               = db.Column(db.Integer)
    position          = db.Column(db.String(50))
    team_id           = db.Column(db.Integer, db.ForeignKey('teams.id'))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    team = db.relationship(TeamsModel)
