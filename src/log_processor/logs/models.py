from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class NginxLog(models.Model):
    time = models.DateTimeField('event time', editable=False, db_index=True)
    remote_ip = models.GenericIPAddressField('source ip address', editable=False, db_index=True)
    method = models.CharField('http method', editable=False, max_length=10)
    uri = models.URLField('requested uri', editable=False, db_index=True)
    response_status_code = models.PositiveSmallIntegerField(
        'response status code', editable=False, validators=[MinValueValidator(100), MaxValueValidator(599)],
    )
    response_size = models.PositiveIntegerField('response size', editable=False)

    class Meta:
        verbose_name = 'Parsed nginx log'
        verbose_name_plural = 'Parsed nginx logs'
