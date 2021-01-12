from reverse.core import utils, MysqlService
from reverse.core._abstract import DatabaseAbstract, DatabaseType
#Gen
import mysql.connector
import json

class DatabaseMLA():

	def __init__(self, db:DatabaseAbstract) -> None:
		self.db = db

	def getUsers(self) -> any:
		_sql = "SELECT * FROM USERS"
		self.cursor.execute(_sql)
		return self.cursor
	
	def getCursor(self) -> any:
		self.cursor = self.db.getCursor()
		return self.cursor
	
	def createConnector(self, *args, **kwargs):
		self.connection = self.db.createConnector(*args, **kwargs)
		return self.connection