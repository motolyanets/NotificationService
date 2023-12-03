from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    phone_regex = RegexValidator(regex=r'^7[0-9]{10}$',
                                 message="Phone number must be entered in the format: '7хххххххххх'. Need 12 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    tag = models.CharField(db_index=True)
    timezone = models.CharField()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.pk)

    @property
    def mobile_operator_code(self):
        phone_number = self.phone_number
        mobile_operator_code = phone_number[1:4]
        return int(mobile_operator_code)
