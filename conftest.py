"""pytest has a special rule: any fixture defined in conftest.py is automatically available to every test file — without importing it. You don't have to do anything. pytest finds it on its own.
Think of conftest.py as the shared kitchen of your test framework. Individual test files are like cooks — they don't bring their own stove. They just walk into the kitchen and use what's there."""

"""
To get a token → we need to LOGIN
To login → the user must EXIST
To exist → we need to CREATE the user first
"""
import pytest
import requests
from config.config import config


@pytest.fixture(scope="session")
def base_url():
    return config.BASE_URL

@pytest.fixture(scope="session")
def registered_user():
    # ---- SETUP ----
    url = f"{config.BASE_URL}/api/public/users"
    payload = {
        "firstName": config.TEST_FIRST_NAME,
        "lastName": config.TEST_LAST_NAME,
        "email": config.TEST_USER_EMAIL,
        "password": config.TEST_USER_PASSWORD
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"User creation failed: {response.text}"

    # ---- HAND OVER DATA ----
    yield {
        "email": config.TEST_USER_EMAIL,
        "password": config.TEST_USER_PASSWORD
    }

    # ---- TEARDOWN ----
    # We need a fresh token to delete the account
    login_url = f"{config.BASE_URL}/api/public/users/login"
    login_response = requests.post(login_url, json={
        "email": config.TEST_USER_EMAIL,
        "password": config.TEST_USER_PASSWORD
    })
    token = login_response.json().get("token")

    delete_url = f"{config.BASE_URL}/api/public/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(delete_url, headers=headers)

@pytest.fixture(scope="session")
def auth_token(registered_user):
    url = f"{config.BASE_URL}/api/public/users/login"
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["token"]
