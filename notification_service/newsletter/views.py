import json
from datetime import datetime

import pytz
import requests
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from client.models import Client
from message.models import Message
from newsletter.models import Newsletter
from newsletter.serializers import NewsletterSerializer


def sending_message(newsletter: Newsletter, client: Client):
    response = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{client.pk}',
                             json={"id": client.pk,
                                   "phone": client.phone_number,
                                   "text": newsletter.messages_text
                                   },
                             headers={
                                 "accept": "application/json",
                                 "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHA'
                                                  'iOjE3MzIxODYyODQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im'
                                                  'h0dHBzOi8vdC5tZS9hbmRyZXltb3RvbHlhbmV0cyJ9.tq6pC1gb'
                                                  'wkWXMybLPdI_KEgZ5y1NClayj5HijU9Medc',
                                 "Content - Type": "application / json"}
                             )
    return response


def starting_newsletter(newsletter: Newsletter, clients: list[Client]):
    for client in clients:
        Message(
            dispatch_status='in progress',
            newsletter_id=newsletter,
            client_id=client,
        ).save()

        response = sending_message(newsletter, client)

        message = Message.objects.filter(newsletter_id=newsletter, client_id=client).first()

        if response.json()['message'] == 'OK':
            message.dispatch_status = 'delivered'
            message.save()
            print(f'Message #{message.pk} was delivered')
        else:
            print(f'Message #{message.pk} wasn\'t delivered. It was sent to schedule.')
            interval = IntervalSchedule.objects.get_or_create(every=50, period='seconds')
            PeriodicTask.objects.create(
                name=f'Repeat sending message #{message.pk}',
                task='repeat_sending_message',
                interval=interval[0],
                kwargs=json.dumps({'newsletter_pk': newsletter.pk, 'client_pk': client.pk}),
                start_time=datetime.now(tz=pytz.utc),
            )


class NewsletterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all().order_by('start_time')
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.accepting_newsletter(response)
        return response

    @staticmethod
    def accepting_newsletter(response: Response):
        clients = Client.objects.all().filter(tag=response.data['client_filter'])
        newsletter = Newsletter.objects.filter(pk=response.data['id']).first()

        if newsletter.start_time <= datetime.now(tz=pytz.utc) <= newsletter.finish_time:
            starting_newsletter(newsletter, clients)
        elif newsletter.start_time >= datetime.now(tz=pytz.utc):
            # Код для отложенной старта рассылки
            pass



