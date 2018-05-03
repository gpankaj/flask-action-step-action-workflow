from src_1.db import db
from src_1.models.action import ActionModel

import datetime

class TaskStepChildrenModel(db.Model):

    __tablename__ = 'task_step_children'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    # a task has step_id, a step has child_step_ids
    # taskid    stepid  next_step_id   type
    #  1        1           2         root
    #  1        2           3         child
    #  1        1           3         root
    #

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    next_step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))

    type = db.Column(db.String(64)) # type of task id, root, child, term , default is root

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, step_id, task_id, next_step_id, type):
        self.task_id = task_id
        self.step_id = step_id
        self.next_step_id = next_step_id

        self.type = type


    def json(self):
        return {'step_id' : self.step_id, 'task_id': self.task_id,'next_step_id': self.next_step_id, 'type': self.type}

    def update_properties(self, step_id, task_id, next_step_id, type):

        self.step_id = step_id
        self.task_id = task_id
        self.next_step_id = next_step_id
        self.type = type

    @classmethod
    def find_by_id(cls, id):
        print("Searching by id (Primary Key) in task_step_children (many entries)", id)
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
    def find_by_step_id_task_type(cls, step_id,task_type):
        print("Searching by task id (many entries)", step_id)
        return cls.query.filter_by(step_id=step_id).filter_by(task_type=task_type).all()

    # create - C
    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()