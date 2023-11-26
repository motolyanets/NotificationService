from django.db import models


class Client(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    mobile_operator_code = models.CharField(max_length=3)
    tag = models.CharField()
    timezone = models.CharField()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.phone_number
