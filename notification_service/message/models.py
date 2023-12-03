from django.db import models

from user.models import User
from newsletter.models import Newsletter


class Message(models.Model):
    CHOICES = (
        ('in progress', 'In progress'),
        ('delivered', 'Delivered'),
        ('is not delivered', 'Is not delivered'),
    )

    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=CHOICES)
    newsletter_id = models.ForeignKey(Newsletter, related_query_name='messages', on_delete=models.SET_NULL,
                                      db_index=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_index=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        unique_together = ('newsletter_id', 'user_id')

    def __str__(self):
        return str(self.pk)
