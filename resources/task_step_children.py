from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.step import StepModel
from src_1.models.task_step_children import TaskStepChildrenModel
from src_1.lib.validators.validator import Validator

class TaskStepChildren(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self,name):

        task_step_childrenModel = TaskStepChildrenModel.find_by_name(name)

        if (task_step_childrenModel):
            return { 'task': task_step_childrenModel.json()}, 200

        return {'message': 'task step children not found'}, 404



    def post(self,name):
        data = request.get_json(force=True)

        if (not Validator.validate_task_id(data['task_id'])):
            return {'message': 'This is not a valid task id'}, 400
        if (not Validator.validate_step_id(data['step_id'])):
            return {'message': 'This is not a valid step id'}, 400
        if (not Validator.validate_action_id(data['action_id'])):
            return {'message': 'This is not a valid action id'}, 400

        task_step_children_id = TaskStepChildrenModel.find_by_task_step_action_id(data['task_id'], data['step_id'],
                                                                              data['next_step_id'],data['type'])



        if(task_step_children_id):
            return {'message' : 'Task step children with same task step children already exists'}, 400 # because it's clients fault to verify.
        else:
            task_step_childrenModel = TaskStepChildrenModel(data['task_id'], data['step_id'], data['next_step_id'], data['type'])

            try:
                task_step_childrenModel.save_to_db()
            except:
                return {'message' : 'an error occured inserting'}, 500 # internal server error

        return task_step_childrenModel.json(), 201

    def delete(self,id):

        task_step_childrenModel = TaskStepChildrenModel.find_by_id(id)
        if(task_step_childrenModel):
            task_step_childrenModel.delete()

            return {'message': 'Successfully deleted'} , 200
        else:
            return {'message': 'No such task_step_children'} , 404
        #steps = list(filter(lambda x: x['name'] != name, steps))


    def put(self,id):
        data = request.get_json(force=True)

        task_step_action_id = TaskStepChildrenModel.find_by_step_id_task_type(data['task_id'], data['step_id'], data['action_id'],
                                                                              data['type'])
        if(task_step_action_id):
            return {'message': 'An entry with same task_step_action id exists'}, 400

        if(id and TaskStepChildrenModel.find_by_id(id)): # which means an id existing and we need to update
            taskStepActionModel = TaskStepChildrenModel.find_by_id(id)
            taskStepActionModel.update_properties(data['task_id'], data['step_id'],data['action_id'],data['type'])
            return {'task_step_children_type': taskStepActionModel.json()}, 200
        else:
            taskStepChildrenModel = TaskStepChildrenModel(data['task_id'], data['step_id'],data['action_id'],data['type'])
            try:
                taskStepChildrenModel.save_to_db()
            except:
                return {'message': 'an error occured inserting'}, 500  # internal server error
            return {'task_step_children_type': taskStepChildrenModel.json()}, 200  # UPDATE


class TaskStepChildrens(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskStepChildrenModel.query.all()]},200