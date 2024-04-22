import abc
import json
import typing
from collections.abc import Generator, Iterable

from .exceptions import EventParsingError


class BaseParser(metaclass=abc.ABCMeta):
    """Converts raw data to python types"""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def parse(self, content: Iterable[str|bytes], strict: bool = False) -> Generator[typing.Any, None, None]:
        pass


ParserType = typing.TypeVar('ParserType', bound=BaseParser)


class JsonParser(BaseParser):
    name = 'json'

    def parse(self, content: Iterable[str|bytes], strict: bool = False) -> Generator[typing.Any, None, None]:
        for line in content:
            try:
                yield json.loads(line)
            except (json.JSONDecodeError, TypeError) as error:
                if strict:
                    raise EventParsingError(f'Event data is not {self.name}') from error
                continue
