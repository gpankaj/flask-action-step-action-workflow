from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from src_1.security import authenticate, identity
from src_1.resources.user import UserRegister
from src_1.resources.step import Step, Steps
from src_1.resources.task import Task, Tasks
from src_1.resources.action import Action, Actions
from src_1.resources.task_step_action import TaskStepAction,TaskStepActions
from src_1.resources.trigger_time import TriggerTime

from flask_cors import CORS

from src_1.resources.task_step_children import TaskStepChildren,TaskStepChildrens

from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from datetime import timedelta
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'jose'

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app,authenticate,identity) # it creates a new endopint called /auth


api.add_resource(Step,'/step/<string:name>')
api.add_resource(Steps,'/steps')


api.add_resource(Action,'/action/<string:name>')
api.add_resource(Actions,'/actions')


api.add_resource(Task,'/task/<string:name>')
api.add_resource(Tasks,'/tasks')


api.add_resource(TaskStepAction,'/task_step_action/')
api.add_resource(TaskStepActions,'/task_step_actions')

api.add_resource(TaskStepChildren,'/task_step_nextstep/')
api.add_resource(TaskStepChildrens,'/task_step_nextsteps')

api.add_resource(UserRegister,'/register')

if __name__=='__main__':
    from src_1.db import db
    db.init_app(app)
    app.run(port=5000, debug = True)

