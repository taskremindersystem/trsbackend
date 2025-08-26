from flask import request, jsonify
from server.python.database.db_manager import (
    load_tasks,
    add_task,
    update_task,
    delete_task,
    mark_task
)
from server.python.database.model import (
    validate_task_description,
    validate_priority
)

def register_routes(app):
    @app.route("/api/v1/tasks", methods=["GET"])
    def get_tasks():
        tasks = load_tasks()
        return jsonify(tasks)

    @app.route("/api/v1/add/tasks", methods=["POST"])
    def add():
        data = request.json

        title = data.get("title")
        description = data.get("description")
        due_date = data.get("dueDate")
        priority = data.get("priority", "medium").lower()
        status = data.get("status", "pending")

        if not title:
            return jsonify({"status": "error", "message": "Title is required"}), 400

        if description and not validate_task_description(description):
            return jsonify({"status": "error", "message": "Invalid task description"}), 400
        if not validate_priority(priority):
            return jsonify({"status": "error", "message": "Invalid priority"}), 400

        task_id = add_task(title, description, due_date, priority, status)
        return jsonify({"status": "success", "task_id": task_id})

    @app.route("/api/v1/update/<int:task_id>", methods=["PUT"])
    def update(task_id):
        data = request.json

        title = data.get("title")
        description = data.get("description")
        due_date = data.get("dueDate")
        priority = data.get("priority", "medium").lower()
        status = "completed" if data.get("completed", False) else "pending"

        if not title:
            return jsonify({"status": "error", "message": "Title is required"}), 400

        if description and not validate_task_description(description):
            return jsonify({"status": "error", "message": "Invalid task description"}), 400
        if not validate_priority(priority):
            return jsonify({"status": "error", "message": "Invalid priority"}), 400

        try:
            updated = update_task(task_id, title, description, due_date, priority, status)
            if updated:
                return jsonify({"status": "success"})
            return jsonify({"status": "error", "message": "Task not found"}), 404
        except Exception as e:
            print(f"Error updating task {task_id}: {str(e)}")
            return jsonify({"status": "error", "message": f"Failed to update task: {str(e)}"}), 500

    @app.route("/api/v1/delete/<int:task_id>", methods=["DELETE"])
    def delete(task_id):
        deleted = delete_task(task_id)
        if deleted:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404

    @app.route("/api/v1/complete/<int:task_id>", methods=["PUT"])
    def complete(task_id):
        marked = mark_task(task_id, True)
        if marked:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404

    @app.route("/api/v1/incomplete/<int:task_id>", methods=["PUT"])
    def incomplete(task_id):
        marked = mark_task(task_id, False)
        if marked:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404