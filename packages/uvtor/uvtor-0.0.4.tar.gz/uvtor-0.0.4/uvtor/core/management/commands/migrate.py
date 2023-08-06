from uvtor.core.management.base import BaseCommand
from uvtor.conf import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import psycopg2
import random
import traceback
import json
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--env', '-e', type=str,
                            help='Env.', default='TEST')
        parser.add_argument(
            '--commit', '-c',
            help=('Commit the migrate'),
            action='store_true'
        )

    def _get_conn(self, ENV='TEST'):

        conf = getattr(settings, 'ENVS')[ENV]
        con = psycopg2.connect(database=conf.get('database'), user=conf.get(
            'user'), host=conf.get('host'), password=conf.get('password'))
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return con

    def _get_range(self, env):
        _filename = os.path.join(
            settings.ROOT_DIR, 'models', 'migrations', f'.{env}')
        if os.path.exists(_filename):
            with open(_filename) as _f:
                _operations = json.load(_f)
        else:
            _operations = []
        if len(_operations) > 0:
            _last = _operations[-1]
            _last_index = _last.get('to')
        else:
            _last_index = -1
        _files = {int(_file.split('_')[0]): _file for _file in
                  os.listdir(os.path.join(
                      settings.ROOT_DIR, 'models', 'migrations'))
                  if _file.split('_')[0].isdigit()}
        _start = _last_index + 1
        _end = len(_files)
        if self._commit:
            _operations.append(
                {
                    'from': _start,
                    'to': _end,
                    'time': str(datetime.datetime.now())
                }
            )
            with open(_filename, 'w') as _f:
                _f.write(json.dumps(_operations))
        return _start, _end

    def _run(self, env, _range):
        _con = self._get_conn(env)
        _con.autocommit = False
        _con.tpc_begin(str.format('dbapi20:{id}', id=random.randint(0, 100)))
        _cur = _con.cursor()
        files = {int(_file.split('_')[0]): _file for _file in
                 os.listdir(os.path.join(
                     settings.ROOT_DIR, 'models', 'migrations'))
                 if _file.split('_')[0].isdigit()}
        start, end = self._get_range(env)
        if start >= end:
            print('Nothing to migrate')
        try:
            for i in range(start, end):
                _migration = __import__(
                    "%s.%s.%s" %
                    ('models', 'migrations', ''.join(
                        files.get(i).split('.')[
                            :-1])), fromlist='migrations')
                for _e in _migration.expressions:
                    _cur.execute(_e)
                print('Migrate', files.get(i))
        except psycopg2.ProgrammingError:
            print(traceback.format_exc())
            print(_migration, 'failed')
        finally:
            if self._commit:
                _con.tpc_commit()
            _con.close()

    def execute(self, **options):
        _env = options.get('env')
        self._commit = options.get('commit')
        print('Using env %s' % _env)
        _run = options.get('range')
        self._run(_env, _run)
