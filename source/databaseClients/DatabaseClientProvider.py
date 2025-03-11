from .PostgresClient import *
from .Psycopg2Client import *
from .SqlServerClient import *
from .InfluxClient import *
from .OracleClient import *

class DatabaseClientProvider ():

	@staticmethod
	def getDatabaseClient (driver:str) -> Any:
		match driver:
			case 'postgres':
				return PostgresClient()
			case 'psycopg2':
				return Psycopg2Client()
