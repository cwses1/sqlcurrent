import pymssql
from .DatabaseClientBase import *

class PymssqlClient (DatabaseClientBase):

	def __init__ (self):
		super().__init__()
		self.server:str = None
		self.userId:str = None
		self.password:str = None
		self.database:str = None
		self.autocommit:bool = None

	def init (self):
		super().init()

		components = self.connString.split(';')
		for component in components:
			componentPair = component.split('=')
			componentName = componentPair[0]
			componentNameLower = componentName.lower()

			if componentNameLower == 'server':
				self.server = componentPair[1]
			elif componentNameLower == 'user':
				self.userId = componentPair[1]
			elif componentNameLower == 'password':
				self.password = componentPair[1]
			elif componentNameLower == 'database':
				self.database = componentPair[1]
			elif componentNameLower == 'autocommit':
				self.autocommit = componentPair[1] == '1'
			else:
				print('Warning, SQL Server connection string parameter string {0} not currently supported.'.format(componentName))

	def executeScriptText (self, scriptText:str):
		with pymssql.connect(server = self.server, user = self.userId, password = self.password, database = self.database, autocommit = self.autocommit) as conn:
			with conn.cursor() as cursor:
				cursor.execute(scriptText)

	def executeResultSet (self, scriptText:str):
		with pymssql.connect(server = self.server, user = self.userId, password = self.password, database = self.database, autocommit = self.autocommit) as conn:
			with conn.cursor() as cursor:
				cursor.execute(scriptText)
				return cursor.fetchone()
