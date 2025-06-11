import pymssql
from .DatabaseClientBase import *

class PymssqlClient (DatabaseClientBase):

	def executeScriptText (self, scriptText:str):
		with pymssql.connect('192.168.10.18', 'heavywork_app', '9834509834iudvnhSFDGHUIzmvajdopFG823u489yv87qwymnrop8eDYTUYOIs7bvtiuahfpqi', 'heavywork_demo') as conn:
			with conn.cursor(as_dict=True) as cursor:
				cursor.execute(scriptText)
			conn.close()

	def executeResultSet (self, scriptText:str):
		with pymssql.connect(self.connString) as conn:
			with conn.cursor(as_dict=True) as cursor:
				cursor.execute(scriptText)
				return cursor.fetchone()
			conn.close()
