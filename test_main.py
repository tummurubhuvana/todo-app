import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def clear_todos():
    main.todos.clear()
    yield
    main.todos.clear()


def test_home_returns_welcome_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API!"}


def test_get_todos_is_empty_at_start():
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_create_todo_defaults_completed_to_false():
    response = client.post("/todos", json={"title": "Buy milk"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Todo created successfully",
        "todo": {"title": "Buy milk", "completed": False},
    }
    assert main.todos[0].title == "Buy milk"
    assert main.todos[0].completed is False


def test_create_todo_keeps_completed_true():
    response = client.post(
        "/todos",
        json={"title": "Write tests", "completed": True},
    )

    assert response.status_code == 200
    assert response.json()["todo"] == {
        "title": "Write tests",
        "completed": True,
    }


def test_create_todo_rejects_missing_title():
    response = client.post("/todos", json={"completed": False})

    assert response.status_code == 422


def test_get_todos_returns_created_items_in_order():
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second", "completed": True})

    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == [
        {"title": "First", "completed": False},
        {"title": "Second", "completed": True},
    ]


def test_delete_todo_removes_item_by_index():
    client.post("/todos", json={"title": "Keep"})
    client.post("/todos", json={"title": "Remove"})

    response = client.delete("/todos/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Todo deleted successfully",
        "todo": {"title": "Remove", "completed": False},
    }
    assert client.get("/todos").json() == [
        {"title": "Keep", "completed": False},
    ]


def test_delete_todo_not_found_for_out_of_range_index():
    client.post("/todos", json={"title": "Only one"})

    response = client.delete("/todos/5")

    assert response.status_code == 200
    assert response.json() == {"error": "Todo not found"}
    assert len(main.todos) == 1


def test_delete_todo_not_found_for_negative_index():
    client.post("/todos", json={"title": "Only one"})

    response = client.delete("/todos/-1")

    assert response.status_code == 200
    assert response.json() == {"error": "Todo not found"}
    assert len(main.todos) == 1


def test_delete_todo_not_found_when_list_is_empty():
    response = client.delete("/todos/0")

    assert response.status_code == 200
    assert response.json() == {"error": "Todo not found"}
