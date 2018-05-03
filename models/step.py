from src_1.db import db
import datetime

#tasks_steps = db.Table('tasks_steps', db.Model.metadata,
#                                    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
#                                    db.Column('step_id', db.Integer, db.ForeignKey('steps.id')),
#                                    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')))

class StepModel(db.Model):

    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))


    description = db.Column(db.String(128))

    message_user = db.Column(db.String(128))
    error_message = db.Column(db.String(128))
    success_message = db.Column(db.String(128))

    #previous_steps = db.Column(db.String) # if previous step is 0 means this is the first step.
                                          # this is comma seperated list of steps.

    next_steps = db.Column(db.String(64)) # there can be multiple next step

    #subscriptions = db.relationship('TaskModel', secondary=tasks_steps,
    #                                backref=db.backref('subscribers', lazy='dynamic'))

    reg_ex = db.Column(db.String) # look for this reg_ex to run this step. applicable when multiple steps are there, if only one step then regex is not checked for.
                                    #  This can be a patten in the previous step's action output

    public = db.Column(db.Boolean) # can be shared with others.
    active = db.Column(db.Boolean) # Executed only if active.

    user_id = db.Column(db.ForeignKey('users.id'))

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    triggertime = db.Column(db.ForeignKey('triggertime.id'),nullable=False)

    #step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))


    #childrens = db.relationship("StepModel",remote_side=[id])

    def __init__(self, name, description, message_user, error_message, success_message, reg_ex, public, active, user_id, trigger_time):
        self.name = name
        self.description = description

        self.message_user = message_user # by default show this message to user.
        self.error_message = error_message # show this message if action returns an error
        self.success_message = success_message # show this message if action returns success.

        self.reg_ex = reg_ex

        self.public = public
        self.active = active

        self.trigger_time = trigger_time

    def json(self):
        return {'name' : self.name, 'description': self.description,'message_user': self.message_user, 'error_message': self.error_message,
                'success_message': self.success_message, 'public': self.public, 'active' : self.active, 'user_id': self.user_id,
                'trigger_time': self.trigger_time}

    def update_properties(self,name,description,message_user,error_message,success_message,public,active, user_id, trigger_time):
        self.name = name
        self.description = description
        self.public = public

        self.active = active
        self.message_user = message_user
        self.error_message = error_message
        self.success_message = success_message
        self.user_id = user_id
        self.trigger_time = trigger_time

    @classmethod
    def find_by_name(cls,name):
        print ("searching by name ", cls.query.filter_by(name=name).first())
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        print("searching by id ", cls.query.filter_by(id=id).first())
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        print("searching by user_id ", cls.query.filter_by(user_id=user_id).all())
        return cls.query.filter_by(user_id=user_id).all()


    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
class PredecessorStepModel(StepModel):
    __tablename__ = "predecessor"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    #predecessor_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    predecessors = db.relationship("StepModel",backref='predecessor', lazy=True)

    def __init__(self, step_id,predecessors=[]):
        self.step_id = step_id
        self.predecessors = predecessors


    def json(self):
        return {'id' : self.step_id, 'predecessors': self.predecessors}


    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()

"""
"""Define constructor and other methods for this class to be able to save to db, update, delete, find etc"""

"""
    @classmethod
    def find_by_id(cls,id):
        print("searching for ", StepModel.query.filter_by(id=id).first())
        return StepModel.query.filter_by(id=id).first()



class SuccessorStepModel(StepModel):
    __tablename__ = "successor"
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    successors = db.relationship("StepModel",backref='successor', lazy=True)
"""