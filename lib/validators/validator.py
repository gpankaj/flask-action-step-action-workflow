from src_1.models.task import TaskModel
from src_1.models.step import StepModel
from src_1.models.action import ActionModel
from src_1.models.task_step_action import TaskStepActionModel
from src_1.models.task_step_children import TaskStepChildrenModel

class Validator():
    @classmethod
    def validate_task_id(cls, task_id):
        print("Searching by task id ", task_id)
        return TaskModel.query.filter_by(id=task_id).first()

    @classmethod
    def validate_step_id(cls, step_id):
        print("Searching by step id ", step_id)
        return StepModel.query.filter_by(id=step_id).first()

    @classmethod
    def validate_action_id(cls, action_id):
        print("Searching by action id ", action_id)
        return ActionModel.query.filter_by(id=action_id).first()