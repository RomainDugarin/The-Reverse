from reverse.core import utils
from reverse.core._abstract import DatabaseAbstract, DatabaseType
#Gen
import mysql.connector
import json

class MysqlService(DatabaseAbstract):

	NAME = DatabaseType.MYSQL

	def __init__(self) -> None:
		super().__init__()

	def _execute(self, operation: str, paramaters:list = []) -> any:
		return self.connection.cursor().execute(operation)
	
	def getCursor(self) -> any:
		return self.connection.cursor()
		
	def createConnector(self, *args, **kwargs):
		self.connection = mysql.connector.connect(*args, **kwargs)
		return self.connection