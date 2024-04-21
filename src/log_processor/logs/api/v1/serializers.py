from rest_framework import serializers

from log_processor.logs.models import NginxLog


class NginxLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NginxLog
        fields = '__all__'
