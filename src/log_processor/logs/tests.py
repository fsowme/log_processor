import io
from collections.abc import Generator
from unittest import mock

from django.test import TestCase

from .models import NginxLog
from .utils.loaders.exceptions import EventParsingError, InvalidEventFormat, LoaderNotFound, NotFoundError, \
    ParserNotRegistered, ReaderNotRegistered, ReadingError
from .utils.loaders.loaders import NginxLoader, get_loader_klass
from .utils.loaders.parsers import JsonParser
from .utils.loaders.readers import FileReader


class FileReaderTestCase(TestCase):
    def test_file_not_found(self):
        with self.assertRaises(NotFoundError):
            with FileReader('invalid_path/file.txt') as f:
                f.read()

    def test_reading_error(self):
        with mock.patch('builtins.open', mock.mock_open()) as mocked_open:
            mocked_open.side_effect = ValueError()
            with self.assertRaises(ReadingError):
                with FileReader('file.txt') as f:
                    f.read()


class JsonParserTestCase(TestCase):
    def setUp(self):
        self.valid_data = ['{"a": [0, 1, 2], "b": 3, "c": {"d": 4}}']
        self.invalid_data = [self.valid_data[0] + 'error']

    def test_ok(self):
        res = JsonParser().parse(self.valid_data)
        self.assertIsInstance(res, Generator)

    def test_invalid_data(self):
        with self.assertRaises(EventParsingError):
            list(JsonParser().parse(self.invalid_data, True))


class LoaderTestCase(TestCase):
    def test_get_loader_klass(self):
        with self.assertRaises(LoaderNotFound):
            get_loader_klass('name')


class NginxLoaderTestCase(TestCase):
    @mock.patch.object(NginxLoader, 'parser_classes', return_value=['csv'])
    def test_parser_not_registered(self, _):
        with self.assertRaises(ParserNotRegistered):
            NginxLoader('file', 'json')

    @mock.patch.object(NginxLoader, 'reader_classes', return_value=['http'])
    def test_reader_not_registered(self, _):
        with self.assertRaises(ReaderNotRegistered):
            NginxLoader('file', 'json')

    @mock.patch.object(FileReader, 'get_content')
    def test_invalid_event_format(self, mocked_get_content):
        buf = io.StringIO()
        buf.write('{"time": "17/May/2015:08:05:32 +0000"}')
        buf.seek(0)
        mocked_get_content.return_value = buf
        with self.assertRaises(InvalidEventFormat):
            NginxLoader(FileReader.name, JsonParser.name).load('', True)

    @mock.patch.object(FileReader, 'get_content')
    def test_ok(self, mocked_get_content):
        valid_event = ('{"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3",'
                       ' "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0}')
        buf = io.StringIO()
        buf.write(valid_event)
        buf.seek(0)
        mocked_get_content.return_value = buf

        count_logs = NginxLog.objects.count()
        NginxLoader(FileReader.name, JsonParser.name).load('', True)
        self.assertEqual(NginxLog.objects.count(), count_logs + 1)
