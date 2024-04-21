from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from log_processor.logs.models import NginxLog
from .serializers import NginxLogSerializer


class NginxLogViewSet(ListModelMixin, GenericViewSet):
    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
