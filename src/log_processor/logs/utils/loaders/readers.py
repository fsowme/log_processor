import abc
import typing

from .exceptions import NotFoundError, ReadingError


class BaseReader(metaclass=abc.ABCMeta):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def get_content(self) -> typing.IO:
        pass

    @abc.abstractmethod
    def on_exit(self) -> None:
        pass

    def __enter__(self) -> typing.IO:
        self.content = self.get_content()
        return self.content

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.on_exit()


ReaderType = typing.TypeVar('ReaderType', bound=BaseReader)


class FileReader(BaseReader):
    name = 'file'
    _mode = 'r'

    def get_content(self) -> typing.IO:
        try:
            return open(self.file_path, self._mode)
        except ValueError as error:
            raise ReadingError('File encoding error') from error
        except FileNotFoundError as error:
            raise NotFoundError('File not found') from error

    def on_exit(self) -> None:
        self.content.close()
