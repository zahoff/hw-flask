from datetime import datetime

import requests

from tests.config import API_URL


def test_root():
    response = requests.get(API_URL)
    assert response.status_code == 404


def test_get_user_by_id(create_user):
    new_user = create_user
    response = requests.get(f'{API_URL}/users/{new_user["id"]}')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['email'] == new_user['email']


def test_get_user_not_exist():
    response = requests.get(f'{API_URL}/users/9999999')
    assert response.status_code == 404


def test_create_user(create_user):
    response = requests.post(f'{API_URL}/users/', json={'email': 'some@mail.com', 'password': 'somepwd'})
    assert response.status_code == 200
    json_data = response.json()
    assert 'id' in json_data
    assert json_data['email'] == 'some@mail.com'


def test_create_user_same_email(create_user):
    response = requests.post(f'{API_URL}/users', json={'email': 'same@mail.com', 'password': 'somepwd'})
    response = requests.post(f'{API_URL}/users', json={'email': 'same@mail.com', 'password': 'somepwd'})
    assert response.status_code == 400
    json_data = response.json()
    assert json_data['message'] == 'email is busy'


def test_delete_user(create_user):
    response = requests.delete(f'{API_URL}/users/{create_user["id"]}')
    assert response.status_code == 403


def test_create_advt(create_user):
    response = requests.post(f'{API_URL}/advts/', json={'title': 'Собачья клетка',
                                                       'description': 'Большая, для немца идеально',
                                                       'user_id': create_user['id']})
    assert response.status_code == 200
    json_data = response.json()
    assert 'title' in json_data
    assert json_data['title'] == 'Собачья клетка'


def test_get_advt_by_id(create_advt):
    response = requests.get(f'{API_URL}/advts/{create_advt["id"]}')
    print(f' ответ = {response}')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == create_advt["title"]


def test_delete_advertisemen(create_advt):
    response = requests.delete(f'{API_URL}/advts/{create_advt["id"]}') # , auth=(create_advt["user_email"], '1234')
    print(f' ответ = {response}')
    assert response.status_code == 403