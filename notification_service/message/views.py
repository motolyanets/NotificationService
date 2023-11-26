from rest_framework.viewsets import ModelViewSet

from message.models import Message
from message.serializers import MessageSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all().order_by('pk')
    serializer_class = MessageSerializer
