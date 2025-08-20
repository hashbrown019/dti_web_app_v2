import mysql.connector as connects # TEMPORARY DISABLED
import sqlite3
import socket
import re
import mysql.connector
from mysql.connector import errorcode

class sqlite:
	def __init__(self, database):
		super(sqlite, self).__init__()
		self.database=database

	def init_db(self):
		conn = None
		try:
			conn = sqlite3.connect(self.database)
			# print("<<<<<<<<< SQLITE INITIALIZATION COMPLETE <<<<<<<<<")
		except Exception as e:
			print(e)
			print("xxxxxxxx ERROR IN SQLITE INITIALIZATION  xxxxxxxx")
		return conn

	def do(self,sql):
		conn = sqlite.init_db(self)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		return cur.lastrowid

	def select(self,sql):
		conn = sqlite.init_db(self)
		conn.row_factory = sqlite.dict_factory
		cur = conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		return rows
		
	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

class mysql:
	def __init__(self, host, user, password, database, use_pure=False):
		'''
			@params: host = Hostname of the database
			@params: user = Username of the database
			@params: password = Password of the database
			@params: database = Database name
			@params: use_pure = Use pure python connection
		'''
		super(mysql, self).__init__()
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.use_pure = use_pure
		self.err_page = 1 

	def info(self):
		return connects

	def init_db(self):
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		mydb = connects.connect(
			host=self.host,
			user=self.user,
			password=self.password,
			database=self.database,
			use_pure=self.use_pure)
		return mydb

	def do(self, sql, params=None):
		conn = None
		cur = None
		try:
			conn = self.init_db()
			cur = conn.cursor()
			cur.execute(sql, params if params else None)
			conn.commit()
			if self.err_page == 1:
				return cur.lastrowid
			else:
				return {"response": "done", "message": cur.lastrowid, "sql": sql}
		except Exception as e:
			if conn:
				conn.rollback()
			return {"response": "error", "message": str(e), "sql": sql}
		finally:
			if cur:
				cur.close()
			if conn:
				conn.close()

	def select(self, sql, params=None, dict_=True):
		conn = None
		cur = None
		try:
			conn = self.init_db()
			cur = conn.cursor(dictionary=dict_)
			cur.execute(sql, params if params else None)
			return cur.fetchall()
		except Exception as e:
			return {"response": "error", "message": str(e), "sql": sql}
		finally:
			if cur:
				cur.close()
			if conn:
				conn.close()

	def insert_or_add_to_db(self, req, table, ids, allowed_fields=None):
		data = dict(req.form)

		if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
			raise ValueError(f"Invalid table name: {table}")
		if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', ids):
			raise ValueError(f"Invalid column name: {ids}")

		if allowed_fields:
			data = {k: v for k, v in data.items() if k in allowed_fields}

		safe_id = data[ids].replace("'", "''")  # Basic SQL injection safety
		is_exist = len(self.select(f"SELECT 1 FROM `{table}` WHERE `{ids}` = '{safe_id}'"))


		if is_exist == 0:
			columns = [f"`{col}`" for col in data.keys()]
			placeholders = ["%s"] * len(data)
			values = list(data.values())
			sql = f"INSERT INTO `{table}` ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
			status = "inserted"
		else:
			set_clause = [f"`{col}` = %s" for col in data.keys()]
			values = list(data.values()) + [data[ids]]
			sql = f"UPDATE `{table}` SET {', '.join(set_clause)} WHERE `{ids}` = %s"
			status = "updated"

		last_row_id = self.do(sql, values)
		return {"lastrowid": last_row_id, "status": status}
		

	# ==========FUNCTION ON MULTIPLE SIMULTANEUS TRANSACTION==========================================
	# function(sql, mysql.init_db(self) )
	# returns a connection that has to be committed before closing transaction
	# conn.commit()

	def db_ready_commit(self,conn):return conn.commit()
	def db_ready(self): # READY for MULTIPLE SIMULTANEUS TRANSACTION
		conn = mysql.init_db(self)
		cur = conn.cursor()
		db_ = {"conn":conn,"cur":cur,"commit":conn.commit}
		return Struct_obj(db_)
		
	def do_(self,sql,db_ready_func):
		if(self.err_page==1):
			db_ready_func.cur.execute(sql)
			return db_ready_func.conn # RETURNS a conn (connection) to close
		else:
			try:
				db_ready_func.cur.execute(sql)
				return db_ready_func.conn # RETURNS a conn (connection) to close
			except Exception as e:
				return {"response":"error","message":str(e), "sql":sql}

	def _select(self,db_ready_func,sql,dict_=True):
		cur = db_ready_func['cur']
		if(self.err_page==1):
			cur.execute(sql)
			rows = cur.fetchall()
			print(rows)
			return rows
		else:
			try:
				# conn = mysql.init_db(self)
				# cur = conn.cursor(dictionary=dict_)
				cur.execute(sql)
				rows = cur.fetchall()
				return rows
			except Exception as e:
				return {"response":"error","message":str(e), "sql":sql}


# ===============================================================================
class Struct_obj:
    def __init__(self, entries):
        self.__dict__.update(**entries)

# =======================================================================

	