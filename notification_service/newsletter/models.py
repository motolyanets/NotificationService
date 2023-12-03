from django.db import models


class Newsletter(models.Model):
    start_time = models.DateTimeField()
    messages_text = models.TextField()
    user_filter = models.CharField()
    finish_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return str(self.pk)
