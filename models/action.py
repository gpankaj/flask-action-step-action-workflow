import sqlite3

from src_1.db import db
import datetime

#steps_actions = db.Table('steps_actions', db.Model.metadata,
#                                    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
#                                    db.Column('action_id', db.Integer, db.ForeignKey('actions.id')),
#                                    db.Column('step_id', db.Integer, db.ForeignKey('steps.id')))


class ActionModel(db.Model):

    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    action_script = db.Column(db.String(256))

    active = db.Column(db.Boolean)

    message_user = db.Column(db.String(1024))
    error_message = db.Column(db.String(1024))
    success_message = db.Column(db.String(1024))
    user_id = db.Column(db.ForeignKey('users.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    #step = db.relationship('StepModel')



    #subscriptions = db.relationship('StepModel',secondary=steps_actions, backref=db.backref('subscribers',lazy='dynamic'))




    #input_parameters = db.Column(db.JSON) # stepname.variablename should give it's value
    #   output_variables = db.Column(db.JSON) # taskname.stepname.variablename should give value
    # provision to define global variables.
    # provision to define step variables.
    # provision to define task variables.

    # provision to autopopulate variables (dynamically)
    #variables = { 'globals' : {'variable' : "X", }, 'task_name': {'variable' : '' , } , 'step_name' : {'variable' : 'value'}}
    # write above dict to storage or cache and keep updating/reading from this.


    def __init__(self, name,action_script, active, message_user, error_message,success_message,user_id):
        self.name = name
        self.action_script = action_script
        self.active = active

        self.message_user = message_user
        self.error_message = error_message
        self.success_message = success_message
        self.user_id = user_id

    def json(self):
        return {'name' : self.name, 'action_script': self.action_script, 'active' : self.active,
                'message_user': self.message_user, 'error_message': self.error_message,'success_message': self.success_message,
                'user_id': self.user_id}


    def update_properties(self,name,action_script,action,active,message_user,error_message,success_message,user_id):
        self.name = name
        self.initial = action_script
        self.action = action
        self.active = active
        self.message_user = message_user
        self.error_message = error_message
        self.success_message = success_message
        self.user_id = user_id

    @classmethod
    def find_by_name(cls,name):
        print ("searching for ", cls.query.filter_by(name=name).first())
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        print("searching for ", cls.query.filter_by(user_id=user_id).all())
        return cls.query.filter_by(user_id=user_id).all()


    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()