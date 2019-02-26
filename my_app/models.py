from datetime import datetime

from sqlalchemy.orm.state import InstanceState

from my_app import db
from my_app.serializer import Serializer


class AbstractModel:
    """
        Abstract class to create models.
    """

    def to_json(self):
        """
            Method that create a JSON of the model's columns with its values serialized.

            Returns
            ----------
            {}
        """
        json = {}
        for key in self.to_dict():
            if type(getattr(self, key)) is not InstanceState:
                json[key] = Serializer.json_serialize(getattr(self, key))
        return json

    def to_dict(self):
        """
            Method that create a dictionary of the model's columns and values.

            Returns
            ----------
            dict
        """
        return dict((column.name, getattr(self, column.name)) for column in self.__table__.columns)

    def __repr__(self):
        """
            Method to create a model's representation with its attributes.

            Returns
            ----------
            String
        """
        return "%s(%r)" % (self.__class__, self.__dict__)


class TeamsModel(db.Model, AbstractModel):
    __tablename__ = 'teams'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name              = db.Column(db.String(255), nullable=False)
    city              = db.Column(db.String(255), nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    players = db.relationship('PlayersModel')


class PlayersModel(db.Model, AbstractModel):
    __tablename__ = 'players'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name              = db.Column(db.String(255))
    age               = db.Column(db.Integer)
    position          = db.Column(db.String(50))
    team_id           = db.Column(db.Integer, db.ForeignKey(TeamsModel.id))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    team = db.relationship(TeamsModel)
