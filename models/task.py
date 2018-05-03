from src_1.db import db
import datetime

class TaskModel(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    reg_ex = db.Column(db.String) # look for this reg_ex to run this step. applicable when multiple steps are there, if only one step then regex is not checked for.
                                    #  This can be a patten in the previous step's action output
    public = db.Column(db.Boolean) # can be shared with others.
    active = db.Column(db.Boolean) # Executed only if active.
    user_id = db.Column(db.ForeignKey('users.id'))

    created_date = db.Column(db.DateTime, default= datetime.datetime.utcnow)


    def __init__(self, name, description, reg_ex, public, active, user_id):
        self.name = name
        self.description = description
        self.reg_ex = reg_ex
        self.public = public
        self.active = active
        self.user_id = user_id

    def json(self):
        return {'name' : self.name, 'description': self.description,'reg_ex': self.reg_ex, 'public': self.public, 'active' : self.active, 'user_id': self.user_id}

    def update_properties(self,name,description, reg_ex,public,active, user_id):
        self.name = name
        self.description = description
        self.reg_ex = reg_ex
        self.public = public
        self.active = active
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
