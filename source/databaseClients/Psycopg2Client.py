from .DatabaseClientBase import *
import psycopg2

class Psycopg2Client (DatabaseClientBase):

	def __init__ (self):
		pass

	def executeScriptText (self, scriptText:str):
		with psycopg2.connect(self.connString) as conn:
			with conn.cursor() as curs:
				curs.execute(scriptText)
			conn.close()

	def executeResultSet (self, scriptText:str):
		with psycopg2.connect(self.connString) as conn:
			with conn.cursor() as cur:
				cur.execute(scriptText)
				return cur.fetchone()
			conn.close()
