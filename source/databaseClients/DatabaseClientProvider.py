from .Psycopg2Client import *
from .InfluxClient import *
from .OracleClient import *
from .PymssqlClient import *

from typing import Any

class DatabaseClientProvider ():

	@staticmethod
	def getDatabaseClient (driver:str) -> Any:
		match driver:
			case 'postgres':
				return Psycopg2Client()
			case 'postgresql':
				return Psycopg2Client()
			case 'psycopg2':
				return Psycopg2Client()
			case 'sqlserver':
				return PymssqlClient()
			case 'mssqlserver':
				return PymssqlClient()
			case 'mssql':
				return PymssqlClient()
			case 'pymssql':
				return PymssqlClient()
			case 'influx':
				return InfluxClient()
