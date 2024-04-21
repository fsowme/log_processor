from django_filters.rest_framework import FilterSet

from log_processor.logs.models import NginxLog


class NginxLogFilterSet(FilterSet):
    class Meta:
        model = NginxLog
        fields = '__all__'
