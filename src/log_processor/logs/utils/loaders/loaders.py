import abc
import typing
from datetime import datetime

from log_processor.logs.models import NginxLog
from .exceptions import InvalidEventFormat, LoaderNotFound, ParserNotRegistered, ReaderNotRegistered
from .parsers import JsonParser, ParserType
from .readers import FileReader, ReaderType


class BaseLoader(metaclass=abc.ABCMeta):
    """Standard loading flow:

    The loader opens and reads the source using one of the readers (BaseReader subclass),
    converts the content into python types using a parser (BaseParser subclass),
    then creates objects of a specific data model"""

    def __init__(self, reader_name: str, parser_name: str) -> None:
        self.reader_class = self._get_reader_class(reader_name)
        self.parser_class = self._get_parser_class(parser_name)

    def load(self, log_path: str, strict: bool = False, batch_size: typing.Optional[int] = None) -> None:
        batch_size = batch_size or self.batch_size
        objects = []
        with self.reader_class(log_path) as content:
            for log_event in self.parser_class().parse(content, strict):
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

    def create_objects(self, objects) -> None:
        self.model.objects.bulk_create(objects)

    @abc.abstractmethod
    def set_instance(self, data: typing.Any):
        pass

    @property
    @abc.abstractmethod
    def model(self):
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def batch_size(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def parser_classes(self) -> list[type[ParserType]]:
        pass

    @property
    @abc.abstractmethod
    def reader_classes(self) -> list[type[ReaderType]]:
        pass

    @classmethod
    def parser_names(cls) -> list[str]:
        return [parser.name for parser in cls.parser_classes]

    @classmethod
    def reader_names(cls) -> list[str]:
        return [reader.name for reader in cls.reader_classes]

    def _get_reader_class(self, name: str) -> type[ReaderType]:
        for reader_class in self.reader_classes:
            if reader_class.name == name:
                return reader_class
        raise ReaderNotRegistered(f'Reader "{name}" is not registered for this log.')

    def _get_parser_class(self, name: str) -> type[ParserType]:
        for parser_class in self.parser_classes:
            if parser_class.name == name:
                return parser_class
        raise ParserNotRegistered(f'Format {name} is not registered for this log')


LoaderType = typing.TypeVar('LoaderType', bound=BaseLoader)


class NginxLoader(BaseLoader):
    name = 'nginx'
    model = NginxLog
    batch_size = 1000
    _time_format = '%d/%b/%Y:%H:%M:%S %z'
    reader_classes = [FileReader]
    parser_classes = [JsonParser]

    def set_instance(self, data: typing.Any):
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


def get_loader_klass(name: str) -> type[LoaderType]:
    try:
        return LOADERS_CLASSES_BY_NAME[name]
    except KeyError:
        raise LoaderNotFound(f'Loader with name "{name}" not found')
