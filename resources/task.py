from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.step import StepModel
from src_1.models.task import TaskModel

class Task(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self,name):

        task = TaskModel.find_by_name(name)

        if (task):
            return { 'task': task.json()}, 200

        return {'message': 'Task not found'}, 404


    def post(self,name):
        data = request.get_json(force=True)

        taskModel = TaskModel.find_by_name(data['name'])


        if(taskModel):
            return {'message' : 'A task with name {} already exists'.format(data['name'])}, 400 # because it's clients fault to verify.
        else:
            taskModel = TaskModel(data['name'], data['description'], data['reg_ex'], data['public'],  data['active'], data['user_id'])


            ######START: This is TBD # work in progress#####
            #action = ActionModel.find_by_name("Added a new Action - 1")
            #stepModel.subscribers.append(action)

            ######END: This is TBD # work in progress#####


            try:
                taskModel.save_to_db()
            except:
                return {'message' : 'an error occured inserting'}, 500 # internal server error

        return taskModel.json(), 201

    def delete(self,name):

        taskModel = TaskModel.find_by_name(name)
        if(taskModel):
            taskModel.delete()

            return {'message': 'Successfully deleted'} , 200
        else:
            return {'message': 'No such step'} , 404
        #steps = list(filter(lambda x: x['name'] != name, steps))




    def put(self, name):
        data = request.get_json(force=True)

        taskModel = TaskModel.find_by_name(name)

        new_name_task = TaskModel.find_by_name(data['name'])


        if(new_name_task == None):
            print("Upserting ", data['name'])
            taskModel = TaskModel(data['name'], data['description'], data['reg_ex'],data['public'], data['active'], data['user_id'])
            try:
                taskModel.save_to_db()
            except:
                return {'message': 'an error occured inserting'}, 500  # internal server error
        if (taskModel != None and new_name_task != None):

            taskModel.update_properties(name, data['description'], data['reg_ex'], data['public'], data['active'], data['user_id'])
            taskModel.save_to_db()

            return {'step': taskModel.json()}
        else:
            if(new_name_task != None):
                return {'message' : 'step with same name already exists'}, 400

        task = TaskModel.find_by_name(data['name']) # find step details after put/rename/insert
        return {'task': task.json()}


class Tasks(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskModel.query.all()]},200