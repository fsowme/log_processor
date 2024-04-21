from rest_framework import status
from rest_framework.reverse import reverse

from log_processor.logs import factories
from log_processor.tools.tests.testcases import APITestCase
from .schemas import NGINX_LOG_SCHEMA_LIST


class NginxLogApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.LIMIT = 2
        cls.url = reverse('nginxlog-list')

    def setUp(self):
        self.logs = factories.NginxLogFactory.create_batch(self.LIMIT)

    def test_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDataSchema(response.data, NGINX_LOG_SCHEMA_LIST)
