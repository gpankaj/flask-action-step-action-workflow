from src_1.db import db
import datetime

class TaskStepActionModel(db.Model):

    __tablename__ = 'task_step_action'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # a task has step_id, a step has
    # taskid    stepid  action_id
    #  1        1           2
    #  1        2           3
    #  1        1           3
    #
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, step_id, task_id, action_id):
        self.task_id = task_id
        self.step_id = step_id
        self.action_id = action_id

    def json(self):
        return { 'step_id' : self.step_id, 'task_id': self.task_id,'action_id': self.action_id }

    def update_properties(self, step_id, task_id, action_id):

        self.step_id = step_id
        self.task_id = task_id
        self.action_id = action_id

    @classmethod
    def find_by_id(cls, id):
        print("Searching by id (Primary Key) in task_step_action (many entries)", id)
        return cls.query.filter_by(id=id).all()

    @classmethod
    def find_by_step_id(cls, step_id):
        print("Searching by step_id id (many entries)", step_id)
        return cls.query.filter_by(step_id=step_id).all()


    @classmethod
    def find_by_task_id(cls,task_id):
        print ("Searching by task id (many entries)", task_id)
        return cls.query.filter_by(task_id=task_id).all()

    @classmethod
    def find_by_action_id(cls,action_id):
        print("Searching by action id (many entries)", action_id)
        return cls.query.filter_by(action_id=action_id).all()



    @classmethod
    def find_by_task_step_action_id(cls, task_id,step_id,action_id):
        print("Searching by find_by_task_step_action_id (many entries)",  task_id,step_id,action_id)
        return cls.query.filter_by(task_id=task_id).filter_by(step_id=step_id).filter_by(action_id=action_id).first()


    # create - C
    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()