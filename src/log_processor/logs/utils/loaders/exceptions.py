class BaseLoaderException(Exception):
    def __init__(self, message):
        self.message = message


class ReaderException(BaseLoaderException):
    pass


class ReadingError(ReaderException):
    pass


class NotFoundError(ReaderException):
    pass


class ParserException(BaseLoaderException):
    pass


class EventParsingError(ParserException):
    pass


class LoaderException(BaseLoaderException):
    pass


class ReaderNotRegistered(LoaderException):
    pass


class ParserNotRegistered(LoaderException):
    pass


class InvalidEventFormat(LoaderException):
    pass


class LoaderNotFound(LoaderException):
    pass
