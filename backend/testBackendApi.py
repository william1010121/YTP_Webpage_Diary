import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Adjust the import based on your project structure

client = TestClient(app)

# Sample valid and invalid payloads for testing

valid_upload_payload = {
    "user": "test_user",
    "url": "https://example.com/file",
    "title": "Test File",
    "content": "This is a test file."
}

invalid_upload_payload = {
    "user": "test_user",
    # "url": "https://example.com/file",  # Missing required field
    "title": "Test File",
    "content": "This is a test file."
}

valid_edit_payload = {
    "user": "test_user",
    "date": "04-30",
    "index": 0,
    "content": "Updated content."
}

invalid_edit_payload = {
    "user": "test_user",
    "date": "04-30",
    # "index": 0,  # Missing required field
    "content": "Updated content."
}

valid_list_payload = {
    "user": "test_user"
}

invalid_list_payload = {
    # "user": "test_user"  # Missing required field
}

def precreate_user_directory(date):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create a user directory before running the test
            import os
            user_directory = "./UserData/test_user"
            os.makedirs(user_directory, exist_ok=True)
            with open(f"{user_directory}/{date}.diary", "w") as f:
                f.write('{"Data": [{"id": 0, "type": "url", "content": "https://example.com/file", "title": "Test File"}], "length": 1}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def test_root_get():
    response = client.get("/")
    assert response.status_code == 200
    # You can add more assertions based on the expected response content
    # For example:
    # assert response.json() == {"message": "Welcome to the FastAPI application"}

def test_upload_url_success():
    response = client.post("/api/uploads/url", json=valid_upload_payload)
    assert response.status_code == 200
    # Add assertions based on the expected successful response
    # For example:
    # assert "id" in response.json()

def test_upload_url_validation_error():
    response = client.post("/api/uploads/url", json=invalid_upload_payload)
    assert response.status_code == 422
    # Verify the structure of the validation error
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)

@precreate_user_directory(date="04-30")
def test_edit_url_success():
    response = client.post("/api/edit/url", json=valid_edit_payload)
    assert response.status_code == 200
    # Add assertions based on the expected successful response

@precreate_user_directory(date="04-30")
def test_edit_url_validation_error():
    response = client.post("/api/edit/url", json=invalid_edit_payload)
    assert response.status_code == 422
    # Verify the structure of the validation error
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)

def test_list_files_success():
    response = client.post("/api/list", json=valid_list_payload)
    assert response.status_code == 200
    # Add assertions based on the expected successful response
    # For example:
    # assert isinstance(response.json(), list)

def test_list_files_validation_error():
    response = client.post("/api/list", json=invalid_list_payload)
    assert response.status_code == 422
    # Verify the structure of the validation error
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)
