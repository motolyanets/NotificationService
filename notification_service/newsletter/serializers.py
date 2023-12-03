from datetime import datetime

import pytz
from rest_framework import serializers

from .models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

    def validate(self, data):
        if data['finish_time'] <= datetime.now(tz=pytz.utc):
            raise serializers.ValidationError('Creating a newsletter that ended in the past is not allowed!')
        if data['finish_time'] <= data['start_time']:
            raise serializers.ValidationError('The start time of the mailing must be earlier than the end time!')
        return data
