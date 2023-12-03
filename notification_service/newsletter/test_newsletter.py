from datetime import datetime, timedelta

import pytest
import pytz
from rest_framework import status


@pytest.mark.django_db
def test_get_newsletters(client, newsletter_factory):
    newsletters = newsletter_factory.create_batch(3)

    resp = client.get('/api/newsletters/')
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == len(newsletters)
    assert sorted([p.id for p in newsletters]) == sorted([data["id"] for data in resp.json()])


@pytest.mark.django_db
def test_create_newsletter(client):
    data = {'start_time': datetime.now(tz=pytz.utc) - timedelta(days=1),
            'messages_text': 'tag',
            'user_filter': 'Europe/Kiev',
            'finish_time': datetime.now(tz=pytz.utc) + timedelta(days=1),
            }

    resp = client.post('/api/newsletters/', data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert datetime.strptime(resp.json()['start_time'], '%Y-%m-%dT%H:%M:%S.%f%z') == data['start_time']
    assert resp.json()['messages_text'] == data['messages_text']
    assert resp.json()['user_filter'] == data['user_filter']
    assert datetime.strptime(resp.json()['finish_time'], '%Y-%m-%dT%H:%M:%S.%f%z') == data['finish_time']


@pytest.mark.django_db
def test_update_newsletter(client, newsletter_factory):
    newsletter = newsletter_factory()
    data = {'start_time': datetime.now(tz=pytz.utc) - timedelta(days=1),
            'messages_text': 'tag',
            'user_filter': 'Europe/Kiev',
            'finish_time': datetime.now(tz=pytz.utc) + timedelta(days=1),
            }

    resp = client.patch(f'/api/newsletters/{newsletter.id}/', data=data)
    assert resp.status_code == status.HTTP_200_OK
    assert datetime.strptime(resp.json()['start_time'], '%Y-%m-%dT%H:%M:%S.%f%z') == data['start_time']
    assert resp.json()['messages_text'] == data['messages_text']
    assert resp.json()['user_filter'] == data['user_filter']
    assert datetime.strptime(resp.json()['finish_time'], '%Y-%m-%dT%H:%M:%S.%f%z') == data['finish_time']


@pytest.mark.django_db
def test_delete_user(client, newsletter_factory):
    newsletter = newsletter_factory()

    resp = client.delete(f'/api/newsletters/{newsletter.id}/')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f'/api/newsletters/{newsletter.id}/')
    assert resp.status_code == status.HTTP_404_NOT_FOUND
