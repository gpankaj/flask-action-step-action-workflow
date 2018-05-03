from flask import request
from flask_restful import Resource, reqparse, marshal, fields
from flask_jwt import jwt_required
import sqlite3
from src_1.models.action import ActionModel
from src_1.models.step import StepModel

class Action(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name', type="string", required=True, help="This field can not be left blank"
    )




