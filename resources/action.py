from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.action import ActionModel

class Action(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name', type="string", required=True, help="This field can not be left blank"
    )

    @jwt_required()
    def get(self,name):

        action = ActionModel.find_by_name(name)

        if (action):
            return { 'step': action.json()}, 200

        return {'message': 'Action not found'}, 404

    def post(self,name):
        data = request.get_json(force=True)

        actionModel = ActionModel.find_by_name(data['name'])
        print (actionModel)
        if(actionModel):
            return {'message' : 'A action with name {} already exists'.format(data['name'])}, 400 # because it's clients fault to verify.
        else:
            actionModel = ActionModel(data['name'], data['action_script'], data['active'] , data['message_user'],
                                      data['error_message'],data['success_message'],data['user_id'])
            try:
                actionModel.save_to_db()
            except:
                return {'message' : 'an error occured inserting'}, 500 # internal server error because it's not users fault, it's our fault.

        return actionModel.json(), 201

    def delete(self,name):
        data = request.get_json(force=True)
        actionModel = ActionModel.find_by_name(data['name'])
        if(actionModel):
            actionModel.delete()

            return {'message': 'Successfully deleted'} , 200
        else:
            return {'message': 'No such action'} , 404


    def put(self, name):
        data = request.get_json(force=True)

        actionModel = ActionModel.find_by_name(name)
        new_name_action = ActionModel.find_by_name(data['name'])


        if(new_name_action == None):
            print("Upserting ", data['name'])
            actionModel = ActionModel(data['name'], data['action_script'], data['action'], data['active'],
                                  data['message_user'], data['error_message'],data['success_message'],data['user_id'])
            try:
                actionModel.save_to_db()
            except:
                return {'message': 'an error occured inserting'}, 500  # internal server error
        if (actionModel != None and new_name_action != None):

            actionModel.update_properties(name, data['action_script'], data['action'], data['active'],
                                      data['message_user'], data['error_message'], data['success_message'],data['user_id'])
            actionModel.save_to_db()

            return {'step': actionModel.json()}
        else:
            if(new_name_action != None):
                return {'message' : 'action with same name already exists'}, 400

        step = ActionModel.find_by_name(data['name']) # find step details after put/rename/insert
        return {'step': step.json()}


class Actions(Resource):
    def get(self):

        return {'actions': [action.json() for action in ActionModel.query.all()]}, 200