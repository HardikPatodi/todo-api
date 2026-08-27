import requests


BASE_URL = "http://127.0.0.1:8000"


def test_get_tasks():
    print("\nGET /tasks")

    response = requests.get(f"{BASE_URL}/tasks")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200


def test_create_task():
    print("\nPOST /tasks")

    data = {
        "title": "Test Task",
        "description": "Testing POST endpoint",
    }

    response = requests.post(
        f"{BASE_URL}/tasks",
        json=data,
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 201

    return response.json()["id"]


def test_update_task(task_id):
    print(f"\nPUT /tasks/{task_id}")

    data = {
        "title": "Updated Test Task",
        "description": "Testing PUT endpoint",
        "completed": True,
    }

    response = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json=data,
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Test Task"
    assert updated_task["description"] == "Testing PUT endpoint"
    assert updated_task["completed"] is True


def test_delete_task(task_id):
    print(f"\nDELETE /tasks/{task_id}")

    response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}"
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200


def test_empty_title():
    print("\nPOST /tasks with empty title")

    data = {
        "title": "",
        "description": "This should fail",
    }

    response = requests.post(
        f"{BASE_URL}/tasks",
        json=data,
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 422


def test_update_nonexistent_task():
    print("\nPUT /tasks/999999")

    data = {
        "title": "Nonexistent Task",
        "description": "This should fail",
        "completed": False,
    }

    response = requests.put(
        f"{BASE_URL}/tasks/999999",
        json=data,
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 404


def test_delete_nonexistent_task():
    print("\nDELETE /tasks/999999")

    response = requests.delete(
        f"{BASE_URL}/tasks/999999"
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 404


if __name__ == "__main__":
    print("Starting To-Do List API tests...")

    # Test GET
    test_get_tasks()

    # Test POST
    task_id = test_create_task()

    # Test PUT
    test_update_task(task_id)

    # Test DELETE
    test_delete_task(task_id)

    # Test validation
    test_empty_title()

    # Test 404 handling
    test_update_nonexistent_task()
    test_delete_nonexistent_task()

    print("\nAll API tests passed successfully!")