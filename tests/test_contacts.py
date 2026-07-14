from wsgiref import headers

import requests
from faker import Faker
from config.config import config


fake = Faker()

created_contact = {}
def test_create_contact(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, json=payload, headers=headers)
    #print(response.text)
    json_response = response.json()
    created_contact.update(json_response)
    print(created_contact)
    assert "id" in json_response, "Response did not return an id"
    assert json_response["firstName"] == payload["firstName"], "firstName doesn't match"
    assert response.status_code == 201


def test_neg_create_contact():
    url = f"{config.BASE_URL}/api/public/contacts"
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


def test_list_contacts(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)
    print(response.text)
    assert response.status_code == 200

def test_list_contacts_by_id(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url+"/"+created_contact["id"], headers=headers)
    print(response.text)
    assert response.status_code == 200

def test_patch_contact(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
         "phone": "555-9999"
    }
    response = requests.patch(url+"/"+created_contact["id"],json=payload, headers=headers)
    print(response.text)
    assert response.status_code == 200

def test_put_contact(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "firstName": "Replaced",
        "lastName": "Record",
        "email": "replaced@example.com",
        "phone": "000-000-0000",
        "city": "Newtown",
    }
    response = requests.put(url+"/"+created_contact["id"],json=payload, headers=headers)
    print(response.text)
    assert response.status_code == 200
    updated = response.json()

    # Fields you sent should match
    assert updated["firstName"] == "Replaced"
    assert updated["city"] == "Newtown"

    # Fields you didn't send should be null (PUT replaces the whole record)
    assert updated["street1"] is None
    assert updated["country"] is None

def test_delete_contact(auth_token):
    url = f"{config.BASE_URL}/api/public/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(url+"/"+created_contact["id"], headers=headers)
    print(response.text)
    assert response.status_code == 204

    get_response = requests.get(url + "/" + created_contact["id"], headers=headers)
    assert get_response.status_code == 404