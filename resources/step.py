from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.step import StepModel
from src_1.models.action import ActionModel

class Step(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name', type="string", required=True, help="This field can not be left blank"
    )

    @jwt_required()
    def get(self,name):

        step = StepModel.find_by_name(name)

        if (step):
            return { 'step': step.json()}, 200

        return {'message': 'Step not found'}, 404


    def post(self,name):
        data = request.get_json(force=True)

        stepModel = StepModel.find_by_name(data['name'])


        if(stepModel):
            return {'message' : 'A step with name {} already exists'.format(data['name'])}, 400 # because it's clients fault to verify.
        else:
            stepModel = StepModel(data['name'], data['description'], data['message_user'],data['error_message'],data['success_message'],
                                  data['reg_ex'], data['public'],  data['active'], data['user_id'])

            #stepModel.type = "child"
            #stepModel.childrens.append(StepModel.find_by_id(1))

            #predecessor = PredecessorStepModel(1)
            #predecessor.predecessors.append(1)

            #print (predecessor.json())

            #predecessor.save_to_db()

            ######START: This is TBD # work in progress#####
            #action = ActionModel.find_by_name("Added a new Action - 1")
            #stepModel.subscribers.append(action)

            ######END: This is TBD # work in progress#####

            #
            #stepModel.predecessors(stepModel)
            #stepModel.predecessors.(1)
            #
            try:
                stepModel.save_to_db()
            except:
                return {'message' : 'an error occured inserting'}, 500 # internal server error

        #steps.append(data)
        #steps.append(step)
        return stepModel.json(), 201

    def delete(self,name):
        data = request.get_json(force=True)
        global steps
        stepModel = StepModel.find_by_name(data[name])
        if(stepModel):
            stepModel.delete()

            return {'message': 'Successfully deleted'} , 200
        else:
            return {'message': 'No such step'} , 404
        #steps = list(filter(lambda x: x['name'] != name, steps))




    def put(self, name):


        data = request.get_json(force=True)
        #data = parser.parse_args()

        # find if item already exists
        #step = next(filter(lambda x: x['name'] == name, steps),None)

        stepModel = StepModel.find_by_name(name)

        new_name_step = StepModel.find_by_name(data['name'])


        if(new_name_step == None):
            print("Upserting ", data['name'])
            stepModel = StepModel(data['name'], data['initial'], data['public'], data['action'], data['active'],
                                  data['message_user'], data['error_message'], data['user_id'])
            try:
                stepModel.save_to_db()
            except:
                return {'message': 'an error occured inserting'}, 500  # internal server error
        if (stepModel != None and new_name_step != None):

            stepModel.update_properties(name, data['initial'], data['public'], data['action'], data['active'],
                                      data['message_user'], data['error_message'])
            stepModel.save_to_db()

            return {'step': stepModel.json()}
        else:
            if(new_name_step != None):
                return {'message' : 'step with same name already exists'}, 400

        step = StepModel.find_by_name(data['name']) # find step details after put/rename/insert
        return {'step': step.json()}


class Steps(Resource):
    def get(self):
        return {'steps': [step.json() for step in StepModel.query.all()]},200