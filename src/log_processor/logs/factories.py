import factory

from log_processor.tools.tests.sampledata import FakeDateTimeBetween
from .models import NginxLog


class NginxLogFactory(factory.django.DjangoModelFactory):
    time = FakeDateTimeBetween(start_date='-10d', end_date='-1d')
    remote_ip = factory.Faker(provider='ipv4_public')
    method = factory.Faker(provider='http_method')
    uri = factory.Faker(provider='uri_path', deep=2)
    response_status_code = factory.Faker(provider='http_status_code')
    response_size = factory.Faker(provider='random_int', min=0, max=1000000000)

    class Meta:
        model = NginxLog
