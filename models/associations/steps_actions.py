from src_1.db import db

class Steps_Actions(db.Model):

    __tablename__ = 'steps_actions'

    steps_actions = db.Table('steps_actions', db.Model.metadata,
                                    db.Column('action_id', db.Integer, db.ForeignKey('actions.id')),
                                    db.Column('step_id', db.Integer, db.ForeignKey('steps.id'))
                                 )