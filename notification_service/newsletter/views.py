import json
import os
from datetime import datetime

import pytz
import requests
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from django_celery_beat.models import PeriodicTask, IntervalSchedule, ClockedSchedule

from user.models import User
from message.models import Message
from newsletter.models import Newsletter
from newsletter.serializers import NewsletterSerializer
from user.views import logger

load_dotenv()


@extend_schema_view(
    create=extend_schema(summary='Create a new newsletter.'),
    retrieve=extend_schema(summary='Get the newsletter.'),
    update=extend_schema(summary='Update the newsletter.'),
    partial_update=extend_schema(summary='Partial update the newsletter.'),
    destroy=extend_schema(summary='Delete the newsletter.'),
    list=extend_schema(summary='Get list of newsletters.'),
)
class NewsletterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f'Newsletter #{response.data["id"]} was updated!')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            logger.info(f'Newsletter #{kwargs["pk"]} was deleted!')
        return response

    def perform_create(self, serializer):
        serializer.save()
        user_filter = serializer.data['user_filter']
        newsletter_id = serializer.data['id']
        try:
            user_filter = int(user_filter)
        except ValueError:
            pass
        logger.info(f'Newsletter #{newsletter_id} was registered!')
        self.accept_newsletter(user_filter, newsletter_id)

    @staticmethod
    def accept_newsletter(user_filter: str | int, newsletter_id: int):
        if isinstance(user_filter, int):
            all_users = User.objects.all()
            users = []
            for user in all_users:
                if user.mobile_operator_code == user_filter:
                    users.append(user)
        else:
            users = User.objects.filter(tag=user_filter)

        users_id = [user.id for user in users]

        newsletter = Newsletter.objects.filter(id=newsletter_id).first()

        if not newsletter:
            raise Exception('Newsletter not found!')

        if newsletter.start_time <= datetime.now(tz=pytz.utc) <= newsletter.finish_time:
            NewsletterViewSet.start_newsletter(newsletter_id, users_id)
        elif newsletter.start_time >= datetime.now(tz=pytz.utc):
            logger.info(f'Newsletter #{newsletter.id} has been sent to the schedule! '
                        f'It starts at {newsletter.start_time}.')
            clock, _ = ClockedSchedule.objects.get_or_create(clocked_time=newsletter.start_time)
            PeriodicTask.objects.create(
                name=f'Delayed start newsletter #{newsletter.id}',
                task='delayed_start_newsletter',
                clocked=clock,
                kwargs=json.dumps({'newsletter_id': newsletter.id, 'users_id': users_id}),
                expires=newsletter.finish_time,
                one_off=True,
            )

        clock, _ = ClockedSchedule.objects.get_or_create(clocked_time=newsletter.finish_time)
        PeriodicTask.objects.create(
            name=f'Check newsletter #{newsletter.id}',
            task='check_newsletter',
            clocked=clock,
            kwargs=json.dumps({'newsletter_id': newsletter.id}),
            one_off=True,
        )

    @staticmethod
    def start_newsletter(newsletter_id: int, users_id: list[int]):
        logger.info(f'Newsletter #{newsletter_id} starts!')
        newsletter = Newsletter.objects.filter(id=newsletter_id).first()
        if not newsletter:
            raise Exception('Newsletter not found!')

        for user_id in users_id:
            user = User.objects.filter(id=user_id).first()
            if not newsletter:
                raise Exception('User not found!')

            message = Message.objects.create(
                status='in progress',
                newsletter_id=newsletter,
                user_id=user
            )

            response = NewsletterViewSet.send_message(newsletter, user)

            if response.json()['message'] == 'OK':
                message.status = 'delivered'
                message.save()
                logger.info(f'Message #{message.id} was delivered to User #{message.user_id_id}')
            else:
                logger.info(f'Message #{message.id} wasn\'t delivered. It was sent to schedule.')
                interval, _ = IntervalSchedule.objects.get_or_create(every=1, period='minutes')
                PeriodicTask.objects.create(
                    name=f'Repeat sending message #{message.id}',
                    task='repeat_sending_message',
                    interval=interval,
                    kwargs=json.dumps({'newsletter_id': newsletter.id, 'user_id': user.id}),
                    start_time=datetime.now(tz=pytz.utc),
                    expires=newsletter.finish_time,
                )

    @staticmethod
    def send_message(newsletter: Newsletter, user: User):
        API_TOKEN = os.getenv('API_TOKEN')
        API_URL = os.getenv('API_URL')

        response = requests.post(url=f'{API_URL}{user.pk}',
                                 json={'id': user.pk,
                                       'phone': user.phone_number,
                                       'text': newsletter.messages_text
                                       },
                                 headers={'Authorization': f'Bearer {API_TOKEN}'}
                                 )
        return response
