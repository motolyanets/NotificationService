from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from message.models import Message
from message.serializers import GeneralStatSerializer, SpecificStatSerializer


@extend_schema_view(
    list=extend_schema(summary='Get general statistics on created newsletters.'),
)
class GeneralStatisticsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Message.objects\
        .values('newsletter_id')\
        .annotate(in_progress=Count('newsletter_id', filter=Q(status='in progress')),
                  delivered=Count('newsletter_id', filter=Q(status='delivered')),
                  is_not_delivered=Count('newsletter_id', filter=Q(status='is not delivered'))
                  )\
        .order_by('newsletter_id')
    serializer_class = GeneralStatSerializer


@extend_schema_view(
    retrieve=extend_schema(summary='Get detailed statistics of messages sent for a specific newsletter.'),
)
class SpecificStatViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects.prefetch_related('user_id')
    serializer_class = SpecificStatSerializer

    def filter_queryset(self, queryset):
        newsletter_id = self.kwargs.get('pk')
        if newsletter_id:
            queryset = queryset.filter(newsletter_id=newsletter_id).order_by('status', 'id')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
