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
