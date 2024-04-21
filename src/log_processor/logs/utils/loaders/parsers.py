import abc
import json
import typing

from .exceptions import EventParsingError


class BaseParser(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def parse(self, content: typing.Any) -> typing.Any:
        pass


class JsonParser(BaseParser):
    name = 'json'

    def parse(self, content: typing.Any, strict: bool = False) -> typing.Any:
        for line in content:
            try:
                yield json.loads(line)
            except (json.JSONDecodeError, TypeError) as error:
                if strict:
                    raise EventParsingError(f'Event data is not {self.name}') from error
                continue
