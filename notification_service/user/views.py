import logging

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(
    create=extend_schema(summary='Create a new user.'),
    retrieve=extend_schema(summary='Get the user.'),
    update=extend_schema(summary='Update the user.'),
    partial_update=extend_schema(summary='Partial update the user.'),
    destroy=extend_schema(summary='Delete the user.'),
    list=extend_schema(summary='Get list of users.'),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            logger.info(f'User #{response.data["id"]} was registered!')
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f'User #{response.data["id"]} was updated!')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            logger.info(f'User #{kwargs["pk"]} was deleted!')
        return response
