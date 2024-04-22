from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from .models import NginxLog


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = ['time', 'remote_ip', 'method', 'uri', 'response_status_code', 'response_size']
    search_fields = ['remote_ip', 'uri']
    list_filter = ['method', 'response_status_code', ('time', DateTimeRangeFilterBuilder())]
