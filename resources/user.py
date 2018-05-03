import sqlite3
from flask import request
from flask_restful import Resource, Api, reqparse
from src_1.models.user import UserModel


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if(UserModel.find_by_username(data['username'])):
            return {'message': 'User already exists'}, 400


        user = UserModel(**data)
        user.save_to_db()


        return {'message' : 'User Created Successfully '}, 201
