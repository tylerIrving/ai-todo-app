import redis
import uuid
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def generate_unique_id():
    return str(uuid.uuid4())


def add_todo_item(session_id, todo_item_data):
    # Store todo item using the cookie data as the key
    redis_client.hset(
        f"todo_items: {session_id}", generate_unique_id(), json.dumps(todo_item_data)
    )


def get_todo_items(session_id):
    # Retrieve all todo items for a specific user
    todo_items = redis_client.hgetall(f"todo_items: {session_id}")

    # Convert the todo item data from JSON strings to dictionaries
    todo_items = {
        k.decode("utf-8"): json.loads(v.decode("utf-8")) for k, v in todo_items.items()
    }

    return todo_items


# def assign_task_to_user(user_id, task_id):
#     redis_client.sadd(f"user:{user_id}:tasks", task_id)


# def get_tasks_for_user(user_id):
#     task_ids = redis_client.smembers(f"user:{user_id}:tasks")
#     tasks = []
#     for task_id in task_ids:
#         task_data = redis_client.hgetall(f"task:{task_id}")
#         tasks.append(task_data)
#     return tasks


# def create_user(session_id):
#     user_data = {
#         "user_id": session_id,
#     }

#     redis_client.hmset(f"user:{session_id}", user_data)
