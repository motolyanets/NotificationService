from rest_framework.viewsets import ModelViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def filter_queryset(self, queryset):
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tag=tag)
        return queryset

