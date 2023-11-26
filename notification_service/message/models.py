from django.db import models

from client.models import Client
from newsletter.models import Newsletter


class Message(models.Model):
    sending_time = models.DateTimeField(auto_now=True)
    dispatch_status = models.CharField()
    newsletter_id = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, null=True)
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.pk
