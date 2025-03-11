from .DatabaseClientBase import *
import psycopg2

class Psycopg2Client (DatabaseClientBase):

	def __init__ (self, connString:str):
		super.__init__(self, connString)

	