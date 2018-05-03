from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required

from src_1.models.trigger_time import TriggerTimeModel

class TriggerTime(Resource):
    #TriggerTimeModel.query.filter_by()
    pass
