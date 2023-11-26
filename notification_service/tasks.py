import requests
from celery import shared_task

from django_celery_beat.models import PeriodicTask

from client.models import Client
from message.models import Message
from newsletter.models import Newsletter


@shared_task(name='repeat_sending_message')
def repeat_sending_message(mes):
    client = Client.objects.filter(pk=mes['client_pk']).first()
    newsletter = Newsletter.objects.filter(pk=mes['newsletter_pk']).first()

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
    message = Message.objects.filter(newsletter_id=newsletter, client_id=client).first()

    if response.json()['message'] == 'OK':
        message.dispatch_status = 'delivered'
        message.save()
        print(f'Message #{message.pk} was delivered')
        task = PeriodicTask.objects.get(name=f'Repeat sending message #{message.pk}')
        task.enabled = False
        task.save()
    else:
        print(f'Message #{message.pk} wasn\'t delivered. It\'ll be sent in 10 seconds.')



