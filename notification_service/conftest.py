import logging

import pytest
import factory
import pytz
from pytest_factoryboy import register
from rest_framework.test import APIClient

from message.models import Message
from newsletter.models import Newsletter
from user.models import User


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture(autouse=True)
def test_foo(caplog):
    caplog.set_level(logging.ERROR)
    pass


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.Faker('pystr_format', string_format='7##########')
    tag = factory.Faker('pystr')
    timezone = factory.Faker('pystr')


@register
class NewsletterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Newsletter

    start_time = factory.Faker('past_datetime', tzinfo=pytz.utc)
    messages_text = factory.Faker('pystr')
    user_filter = factory.Faker('pystr')
    finish_time = factory.Faker('future_datetime', tzinfo=pytz.utc)
