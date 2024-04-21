from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from log_processor.logs.models import NginxLog
from .filters import NginxLogFilterSet
from .serializers import NginxLogSerializer


class NginxLogViewSet(ListModelMixin, GenericViewSet):
    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NginxLogFilterSet
