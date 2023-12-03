import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_users(client, user_factory):
    users = user_factory.create_batch(3)

    resp = client.get('/api/users/')
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == len(users)
    assert sorted([p.id for p in users]) == sorted([data["id"] for data in resp.json()])


@pytest.mark.django_db
def test_create_user(client):
    data = {'phone_number': '71234567891', 'tag': 'tag', 'timezone': 'Europe/Kiev'}

    resp = client.post('/api/users/', data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()['phone_number'] == data['phone_number']
    assert resp.json()['tag'] == data['tag']
    assert resp.json()['timezone'] == data['timezone']


@pytest.mark.django_db
def test_update_user(client, user_factory):
    user = user_factory()
    data = {'phone_number': '71113587412'}

    resp = client.patch(f'/api/users/{user.id}/', data=data)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['phone_number'] == data['phone_number']


@pytest.mark.django_db
def test_delete_user(client, user_factory):
    user = user_factory()

    resp = client.delete(f'/api/users/{user.id}/')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f'/api/users/{user.id}/')
    assert resp.status_code == status.HTTP_404_NOT_FOUND
