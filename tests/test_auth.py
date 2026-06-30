import requests
from config.config import BASE_URL, TEST_USER_EMAIL, TEST_FIRST_NAME, TEST_USER_PASSWORD


def test_login_success(registered_user):
    """Valid credentials should return 200 and a JWT token"""
    url = f"{BASE_URL}/api/public/users/login"
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }

    response = requests.post(url, json=payload)
    json_response = response.json()
    #print(json_response)


    # Assert 1: Did the server accept our request?
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    # Assert 2: Did we get a token back?
    assert "token" in json_response, "Response did not contain a token"

    # Assert 3: Is the token actually a non-empty string?
    assert isinstance(json_response["token"], str), "Token is not a string"
    assert len(json_response["token"]) > 0, "Token is empty"

def test_login_wrong_password():
    """Wrong password should return 401 Unauthorized"""
    url = f"{BASE_URL}/api/public/users/login"
    payload = {
        "email": TEST_USER_EMAIL,
        "password": "WrongPWD"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"

def test_me(auth_token):
    url = f"{BASE_URL}/api/public/users/me"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER_EMAIL, "Email doesn't match"
    assert response.json()["firstName"] == TEST_FIRST_NAME, "First name doesn't match"

#Negative test
def test_me_without_auth():
    url = f"{BASE_URL}/api/public/users/me"
    response = requests.get(url)
    assert response.status_code == 401

def test_update_me(auth_token):
    url = f"{BASE_URL}/api/public/users/me"
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "firstName": "Janet",
        "email": TEST_USER_EMAIL
    }
    response = requests.patch(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER_EMAIL

def test_logout_me():
    login_response = requests.post(f"{BASE_URL}/api/public/users/login", json={
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    })
    token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/public/users/logout", headers=headers)

    assert response.status_code == 200