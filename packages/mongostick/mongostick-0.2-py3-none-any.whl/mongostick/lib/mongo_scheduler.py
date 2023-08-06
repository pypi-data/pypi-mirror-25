import json

import tornado.log
from motor import MotorClient
from tornado.gen import sleep
from tornado.options import options

from mongostick.lib.mongodb_encoder import MongoDBEncoder


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MongoDBScheduler(metaclass=Singleton):
    def __init__(self):
        tornado.log.gen_log.info('Connecting to MongoDB')
        self.client = MotorClient(options.mongodb_url)
        tornado.log.gen_log.info('Connection to MongoDB established')

        self.replica_set_info = json.dumps({
                    'type': 'REPLICA_SET',
                    'data': {
                        'conf': {},
                        'members': [],
                    },
                })
        self._operations = []
        self.operations = json.dumps({
                    'type': 'OPERATIONS',
                    'data': [],
                })
        self._databases = {}
        self.databases = json.dumps({
                    'type': 'DATABASES',
                    'data': [],
                })

    async def update_replica_info(self):
        while True:
            replica_set_info = await self.client.admin.command('replSetGetStatus')
            replica_set_conf = await self.client.admin.command('replSetGetConfig')

            members = {}

            # merge member info
            for member in replica_set_info['members']:
                members[member['_id']] = member
            del replica_set_info['members']

            for member in replica_set_conf['config']['members']:
                members[member['_id']].update(member)
            del replica_set_conf['config']['members']

            # merge settings
            conf = replica_set_info
            conf.update(replica_set_conf['config']['settings'])

            self.replica_set_info = json.dumps(
                {
                    'type': 'REPLICA_SET',
                    'data': {
                        'conf': conf,
                        'members': [m for m in members.values()],
                    },
                }, cls=MongoDBEncoder)

            await sleep(20)

    async def update_data(self):
        while True:
            self._operations = await self.client.local.current_op(True)
            self._operations = self._operations['inprog']
            self.operations = json.dumps(
                {
                    'type': 'OPERATIONS',
                    'data': self._operations,
                },
                cls=MongoDBEncoder
            )

            databases = await self.client.database_names()

            for db_name in databases:
                db = self.client[db_name]
                db_stats = await db.command('dbstats')
                col_names = await db.collection_names()
                col_info = {}

                for col_name in col_names:
                    col_stats = await db.command('collstats', col_name)
                    col_info[col_name] = col_stats

                self._databases[db_name] = {
                    'stats': db_stats,
                    'collections': col_info
                }

            self.databases = json.dumps(
                {
                    'type': 'DATABASES',
                    'data': self._databases,
                }
            )

            await sleep(20)
