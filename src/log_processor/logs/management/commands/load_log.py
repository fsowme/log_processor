from argparse import ArgumentParser, BooleanOptionalAction

from django.core.management.base import BaseCommand

from log_processor.logs.utils.loaders import BaseLoaderException, LOADER_CLASSES, get_loader_klass


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        subparsers = parser.add_subparsers(title='Available loaders', required=True, dest='loader')

        strict_help = ('--strict: stop loading if invalid event data is detected in the source.'
                       ' --no-strict: skip event with error.'
                       ' Default: --no-parse')
        parser.add_argument('--strict', action=BooleanOptionalAction, default=False, help=strict_help)

        for loader_cls in LOADER_CLASSES:
            loader_parser = subparsers.add_parser(loader_cls.name)
            loader_parser.add_argument('--reader', choices=loader_cls.reader_names(), required=True)
            loader_parser.add_argument('--parser', choices=loader_cls.parser_names(), required=True)
            loader_parser.add_argument('--source', required=True)
            loader_parser.add_argument('--batch_size', default=1000, type=int)

    def handle(self, *args, **options):
        try:
            loader_cls = get_loader_klass(options['loader'])
            loader = loader_cls(options['reader'], options['parser'])
            loader.load(options['source'], options['strict'])
        except BaseLoaderException as error:
            print(error.message)
