from rest_framework import serializers
from rest_framework.fields import IntegerField

from .models import Message


class GeneralStatSerializer(serializers.ModelSerializer):
    newsletter_id = IntegerField()
    in_progress = serializers.IntegerField()
    delivered = serializers.IntegerField()
    is_not_delivered = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['newsletter_id', 'in_progress', 'delivered', 'is_not_delivered']


class SpecificStatSerializer(serializers.ModelSerializer):
    user_phone_number = serializers.CharField(source='user_id.phone_number')

    class Meta:
        model = Message
        fields = ['id', 'status', 'user_phone_number', 'created_at']
