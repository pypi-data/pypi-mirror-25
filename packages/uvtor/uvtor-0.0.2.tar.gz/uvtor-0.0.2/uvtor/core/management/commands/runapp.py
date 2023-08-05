from tornado.platform.asyncio import AsyncIOMainLoop
from uvtor.core.management.base import BaseCommand
from uvtor.core import make_app
import asyncio
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

AsyncIOMainLoop().install()


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )
        parser.add_argument(
            '--port', '-P', metavar='port',
            default=8000,
            help='Listen port',
        )

        parser.add_argument(
            '--address', '-H', metavar='address',
            default='127.0.0.1',
            help='Listen address',
        )
        parser.add_argument(
            '--autoreload',
            help='Enable autoreload',
            action='store_true'
        )

    def execute(self, **options):
        _appname = options.get('name')
        _address = options.get('address')
        _port = options.get('port')
        _autoreload = options.get('autoreload')
        _app = make_app(_appname, _autoreload)
        _app.listen(_port, address=_address)
        print(f'Server started, listen on {_address}:{_port}')
        asyncio.get_event_loop().run_forever()
