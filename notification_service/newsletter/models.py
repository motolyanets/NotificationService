from datetime import datetime

import pytz
from django.db import models

from client.models import Client
# from message.models import Message


class Newsletter(models.Model):
    start_time = models.DateTimeField()
    messages_text = models.TextField()
    client_filter = models.CharField()
    finish_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return str(self.pk)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save()
    #     clients = Client.objects.all().filter(tag=self.client_filter)
    #
    #     if self.start_time <= datetime.now(tz=pytz.utc) <= self.finish_time:
    #         for client in clients:
    #             print(client.phone_number)
    #             Message(
    #                 dispatch_status=(i + 1),
    #                 newsletter_id=self,
    #                 client_id=client,
    #             ).save()
