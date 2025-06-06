from .DatabaseClientBase import *
import psycopg2

class Psycopg2Client (DatabaseClientBase):

	def __init__ (self):
		pass

	def runCreateScript (self, createScript:str):
		conn = psycopg2.connect(self.connString)
		with conn:
			with conn.cursor() as curs:
				curs.execute(createScript)
		conn.close()

	def runUpdateScript (self, createScript:str):
		conn = psycopg2.connect(self.connString)
		with conn:
			with conn.cursor() as curs:
				curs.execute(createScript)
		conn.close()

	def runApplyScript (self, createScript:str):
		conn = psycopg2.connect(self.connString)
		with conn:
			with conn.cursor() as curs:
				curs.execute(createScript)
		conn.close()

	def runCheckScript (self, scriptText:str):
		conn = psycopg2.connect(self.connString)
		with conn:
			with conn.cursor() as cur:
				cur.execute(scriptText)
				return cur.fetchone()
		conn.close()

	def runResetScript (self, createScript:str):
		conn = psycopg2.connect(self.connString)
		with conn:
			with conn.cursor() as curs:
				curs.execute(createScript)
		conn.close()
