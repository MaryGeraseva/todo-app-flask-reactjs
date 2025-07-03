from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView
from flaskr.controllers.task_controller import TaskController
from flaskr.schemas.schema import TaskSchema, UpdateTaskSchema

# Blueprint for task-related routes
bp = Blueprint("tasks", __name__)


@bp.route("/tasks")
class Tasks(MethodView):
    """
    Endpoint for creating new tasks.
    Only accessible to authenticated users (JWT required).
    """
    @jwt_required()
    @bp.arguments(TaskSchema)
    @bp.response(201)
    def post(self, data):
        """
        Create a new task for the authenticated user.

        Args:
            data (dict): Task data validated by TaskSchema.

        Returns:
            Response with status 201 on success.
        """
        return TaskController.create(data)


@bp.route("/tasks/user")
class TasksOnUser(MethodView):
    """
    Endpoint for retrieving all tasks belonging to the authenticated user.
    """
    @jwt_required()
    @bp.response(200, TaskSchema(many=True))
    def get(self):
        """
        Get all tasks for the current user.

        Returns:
            List of tasks (serialized by TaskSchema).
        """
        return TaskController.get_all_on_user()


@bp.route("/tasks/<task_id>")
class TaskById(MethodView):
    """
    Endpoint for updating or deleting a specific task by its ID.
    """
    @jwt_required()
    @bp.arguments(UpdateTaskSchema)
    @bp.response(200)
    def put(self, data, task_id):
        """
        Update an existing task.

        Args:
            data (dict): Updated task data validated by UpdateTaskSchema.
            task_id (int): ID of the task to update.

        Returns:
            Response with status 200 on success.
        """
        return TaskController.update(data, task_id)

    @jwt_required()
    @bp.response(204)
    def delete(self, task_id):
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete.

        Returns:
            Empty response with status 204 on success.
        """
        return TaskController.delete(task_id)
