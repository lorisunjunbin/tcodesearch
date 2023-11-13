import logging

from utils import SystemConfig
from datastore.Sqlite3TcodeLiteStore import Sqlite3TcodeLiteStore


class TcodeLiteModel(object):

    db: Sqlite3TcodeLiteStore

    def __init__(self, config: SystemConfig):

        self.sysconfig = config

        # refer to: TcodeLiteconfig.yaml
        self.sysconfig.bind_model(self, ['application'])

        self.db = Sqlite3TcodeLiteStore(self.dbpath)

        logging.info('Initial TcodeLiteModel')

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
