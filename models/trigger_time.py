import datetime
from src_1.db import db

class TriggerTimeModel(db.Model):

    __tablename__ = 'triggertime'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))

    start_date_time = db.Column(db.DateTime)

    active = db.Column(db.Boolean) # Executed only if active.
    user_id = db.Column(db.ForeignKey('users.id'))

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, name, description, start_date_time, active, user_id):
        self.name = name
        self.description = description
        self.start_date_time = start_date_time
        self.active = active
        self.user_id = user_id

    def json(self):
        return {'name' : self.name, 'description': self.description,'start_date_time': self.start_date_time,
                'active' : self.active, 'user_id': self.user_id}

    def update_properties(self,name,description, start_date_time,active, user_id):
        self.name = name
        self.description = description
        self.start_date_time = start_date_time
        self.active = active
        self.user_id = user_id

    def save_to_db(self): # this can insert and update, it's called upserting
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
