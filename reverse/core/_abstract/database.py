from enum import Enum
class DatabaseType:
	MYSQL = "MYSQL"
	SQLITE = "SQLITE3" 

class DatabaseAbstract:

	NAME:str 

	def _execute(self, operation: str, paramaters:list = []) -> any:
		pass

	def getCursor(self) -> any:
		pass

	def createConnector(self, *args, **kwargs) -> any:
		pass