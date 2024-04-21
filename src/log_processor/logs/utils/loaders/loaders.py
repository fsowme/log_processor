import abc
from datetime import datetime

from log_processor.logs.models import NginxLog
from .exceptions import InvalidEventFormat, LoaderNotFound, ParserNotRegistered, ReaderNotRegistered
from .parsers import JsonParser
from .readers import FileReader


class BaseLoader(metaclass=abc.ABCMeta):
    def __init__(self, reader_name, parser_name):
        self.reader = self._get_reader_by_name(reader_name)
        self.parser = self._get_parser_by_name(parser_name)

    def load(self, log_path, strict=False, batch_size: int = None):
        batch_size = batch_size or self.batch_size
        objects = []
        with self.reader(log_path) as content:
            for log_event in self.parser().parse(content, strict):
                try:
                    objects.append(self.set_instance(log_event))
                except InvalidEventFormat:
                    if strict:
                        raise
                    continue
                if len(objects) >= batch_size:
                    self.create_objects(objects)
                    objects = []
            if objects:
                self.create_objects(objects)

    def create_objects(self, objects):
        self.model.objects.bulk_create(objects)

    @abc.abstractmethod
    def set_instance(self, data):
        pass

    @property
    @abc.abstractmethod
    def model(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def batch_size(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def parsers(self) -> list:
        pass

    @property
    @abc.abstractmethod
    def readers(self) -> list:
        pass

    @classmethod
    def parser_names(cls):
        return [parser.name for parser in cls.parsers]

    @classmethod
    def reader_names(cls):
        return [reader.name for reader in cls.readers]

    def _get_reader_by_name(self, name):
        for reader in self.readers:
            if reader.name == name:
                return reader
        raise ReaderNotRegistered(f'Reader "{name}" is not registered for this log.')

    def _get_parser_by_name(self, name):
        for parser in self.parsers:
            if parser.name == name:
                return parser
        raise ParserNotRegistered(f'Format {name} is not registered for this log')


class NginxLoader(BaseLoader):
    name = 'nginx'
    model = NginxLog
    batch_size = 1000
    _time_format = '%d/%b/%Y:%H:%M:%S %z'
    readers = [FileReader]
    parsers = [JsonParser]

    def set_instance(self, data):
        try:
            method, uri, _ = data['request'].split()
            return self.model(
                time=datetime.strptime(data['time'], self._time_format),
                remote_ip=data['remote_ip'],
                method=method,
                uri=uri,
                response_status_code=data['response'],
                response_size=data['bytes']
            )
        except (KeyError, ValueError) as error:
            raise InvalidEventFormat(f'Incorrect event data format found ({data})') from error


LOADER_CLASSES = [NginxLoader]
LOADERS_CLASSES_BY_NAME = {loader.name: loader for loader in LOADER_CLASSES}


def get_loader_klass(name):
    try:
        return LOADERS_CLASSES_BY_NAME[name]
    except KeyError:
        raise LoaderNotFound(f'Loader with name "{name}" not found')
