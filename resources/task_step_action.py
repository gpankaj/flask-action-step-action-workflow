from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.step import StepModel
from src_1.lib.validators.validator import Validator
from src_1.models.task_step_action import TaskStepActionModel
from sqlalchemy.exc import IntegrityError

class TaskStepAction(Resource):
    parser = reqparse.RequestParser()



    def get(self,task_id):

        task_step_actionModel = TaskStepActionModel.find_by_task_id(task_id)

        if (task_step_actionModel):
            return { 'task step action': task_step_actionModel.json()}, 200

        return {'message': 'task_step_action not found'}, 404


    def post(self):
        data = request.get_json(force=True)

        if(not Validator.validate_task_id(data['task_id'])):
            return {'message': 'This is not a valid task id'}, 400
        if(not Validator.validate_step_id(data['step_id'])):
            return {'message': 'This is not a valid step id'}, 400
        if(not Validator.validate_action_id(data['action_id'])):
            return {'message': 'This is not a valid action id'}, 400

        task_step_action_id = TaskStepActionModel.find_by_task_step_action_id(data['task_id'],data['step_id'],data['action_id'])

        if(task_step_action_id):
            return {'message' : 'A task with same task step action id {} already exists'}, 400 # because it's clients fault to verify.
        else:

            task_step_actionModel = TaskStepActionModel(data['task_id'], data['step_id'], data['action_id'])
            try:
                task_step_actionModel.save_to_db()
            except IntegrityError as e:
                return {'message' : 'an integrity error occured inserting ' +str(e)}, 500 # internal server error

        return task_step_actionModel.json(), 201

    def delete(self,id):

        task_step_actionModel = TaskStepActionModel.find_by_id(id)
        if(task_step_actionModel):
            task_step_actionModel.delete()

            return {'message': 'Successfully deleted'} , 200
        else:
            return {'message': 'No such task_step_action'} , 404
        #steps = list(filter(lambda x: x['name'] != name, steps))


    def put(self,id):
        data = request.get_json(force=True)

        task_step_action_id = TaskStepActionModel.find_by_task_step_action_id(data['task_id'], data['step_id'],
                                                                              data['action_id'])
        if(task_step_action_id):
            return {'message': 'An entry with same task_step_action id exists'}, 400

        if(id and TaskStepActionModel.find_by_id(id)): # which means an id existing and we need to update
            taskStepActionModel = TaskStepActionModel.find_by_id(id)
            taskStepActionModel.update_properties(data['task_id'], data['step_id'],data['action_id'])
            return {'task_step_action': taskStepActionModel.json()}, 200
        else:
            taskStepActionModel = TaskStepActionModel(data['task_id'], data['step_id'],data['action_id'])
            try:
                taskStepActionModel.save_to_db()
            except:
                return {'message': 'an error occured inserting'}, 500  # internal server error
            return {'task_step_action': taskStepActionModel.json()}, 200  # UPDATE

class TaskStepActions(Resource):
    def get(self):
        return {'task_step_actions': [task_step_action.json() for task_step_action in TaskStepActionModel.query.all()]},200



