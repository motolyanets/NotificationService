import logging

from celery import shared_task

from django_celery_beat.models import PeriodicTask

from newsletter.views import NewsletterViewSet
from user.models import User
from message.models import Message
from newsletter.models import Newsletter

logger = logging.getLogger(__name__)


@shared_task(name='repeat_sending_message')
def repeat_sending_message(**kwargs):
    newsletter_id = kwargs.get('newsletter_id', None)
    user_id = kwargs.get('user_id', None)

    user = User.objects.filter(id=user_id).first()
    newsletter = Newsletter.objects.filter(id=newsletter_id).first()

    response = NewsletterViewSet.send_message(newsletter, user)

    message = Message.objects.filter(newsletter_id=newsletter, user_id=user).first()

    if response.json()['message'] == 'OK':
        message.status = 'delivered'
        message.save()
        logger.info(f'Message #{message.id} was delivered to User #{message.user_id_id}')
        task = PeriodicTask.objects.get(name=f'Repeat sending message #{message.id}')
        task.enabled = False
        task.save()
    else:
        logger.info(f'Message #{message.id} wasn\'t delivered. It\'ll be sent in 1 minute.')


@shared_task(name='delayed_start_newsletter')
def delayed_start_newsletter(**kwargs):
    newsletter_id = kwargs.get('newsletter_id', None)
    users_id = kwargs.get('users_id', None)
    NewsletterViewSet.start_newsletter(newsletter_id, users_id)


@shared_task(name='check_newsletter')
def check_newsletter(**kwargs):
    newsletter_id = kwargs.get('newsletter_id', None)
    Message.objects.filter(newsletter_id=newsletter_id, status='in progress').update(status='is not delivered')
    logger.info(f'Newsletter #{newsletter_id} was finished!')
