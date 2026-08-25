from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Todo API")


# Todo data structure
class Todo(BaseModel):
    title: str
    completed: bool = False


# Temporary in-memory storage
todos = []


# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Todo API!"}


# Get all todos
@app.get("/todos")
def get_todos():
    return todos


# Add a new todo
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {
        "message": "Todo created successfully",
        "todo": todo
    }


# Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    if todo_id < 0 or todo_id >= len(todos):
        return {"error": "Todo not found"}

    deleted_todo = todos.pop(todo_id)

    return {
        "message": "Todo deleted successfully",
        "todo": deleted_todo
    }