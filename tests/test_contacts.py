import requests
from faker import Faker
from config.config import BASE_URL, TEST_USER_EMAIL

fake = Faker()


def test_create_contact(auth_token):
    url = f"{BASE_URL}/api/public/contacts"
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    json_response = response.json()
    assert "id" in json_response, "Response did not return an id"
    assert json_response["firstName"] == payload["firstName"], "firstName doesn't match"
    assert response.status_code == 201


def test_neg_create_contact():
    url = f"{BASE_URL}/api/public/contacts"
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
    }
    #headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, json=payload)
    assert response.status_code == 401


