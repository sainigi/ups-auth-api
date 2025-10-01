import os
import pyodbc

DBName = os.environ["IdentityDB"]

async def getCursor():
	try:
		conn = pyodbc.connect(DBName)
		cursor = conn.cursor()
		return cursor, conn
	except:
		raise

def getCursorSync():
    try:
        conn = pyodbc.connect(DBName)
        cursor = conn.cursor()
        return cursor, conn
    except:
        raise


