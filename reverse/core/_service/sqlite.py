import sqlite3
from reverse.core import utils

class SqliteService:
    
    __slots__ = [
        'name',
        'instance',
        'dbpath',
        'dbfullpath',
        'env'
    ]

    def __init__(self, dbname = None, dbpath = None):
        self.env = self.getEnvSqlite()
        self.name = self.env['dbname']
        self.dbpath = self.env['dbpath']
        self.dbfullpath = '{}{}'.format(self.dbpath, self.name)
        self.instance = sqlite3.connect(self.dbfullpath)

    def getEnvSqlite(self):
        return utils.load_backend()['sqlite']

    def getDBName(self):
        return self.name
    
    def getInstance(self):
        return self.instance

    def getDBFullpath(self):
        return self.dbfullpath
    
    def getDBPath(self):
        return self.dbpath


