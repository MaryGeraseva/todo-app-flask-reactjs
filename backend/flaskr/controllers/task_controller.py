from typing import Any, Dict, List
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from flaskr.db import db
from flaskr.models.tag_model import TagModel
from flaskr.models.task_model import TaskModel


class TaskController:
    @staticmethod
    def get_all_for_user() -> List[Any]:
        """
        Retrieve all tasks for the current user, including tag names.
        """
        try:
            user_id = get_jwt_identity()
            return (
                db.session.query(
                    TaskModel.id,
                    TaskModel.title,
                    TaskModel.content,
                    TaskModel.status,
                    TaskModel.created_at,
                    TagModel.name.label("tag_name"),
                )
                .filter(TaskModel.user_id == user_id)
                .join(TagModel, TaskModel.tag_id == TagModel.id)
                .all()
            )
        except SQLAlchemyError:
            abort(500, message="Internal server error while fetching user's tasks")

    @staticmethod
    def create(data: Dict[str, Any]) -> None:
        """
        Create a new task for the current user.
        """
        try:
            user_id = get_jwt_identity()
            create_data = {"user_id": user_id, **data}
            new_task = TaskModel(**create_data)
            db.session.add(new_task)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Internal server error while creating task")

    @staticmethod
    def update(task_id: int, data: Dict[str, Any]) -> None:
        """
        Update an existing task by ID.
        """
        try:
            task = db.session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            ).scalar_one()
            task.title = data.get("title", task.title)
            task.content = data.get("content", task.content)
            task.status = data.get("status", task.status)
            db.session.add(task)
            db.session.commit()
        except NoResultFound:
            abort(404, message="Task not found")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Internal server error while updating task")

    @staticmethod
    def delete(task_id: int) -> None:
        """
        Delete a task by ID.
        """
        try:
            task = db.session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            ).scalar_one()
            db.session.delete(task)
            db.session.commit()
        except NoResultFound:
            abort(404, message="Task not found")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Internal server error while deleting task")
