import json
from mysql.connector import Error
from mysql.connector import pooling

import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
database = os.getenv("database")
password = os.getenv("password")

def connectPool(status):
  if status == "setup":
    with open("pwd.json") as f:
      pwd = json.load(f)
  else:
    with open("./data/pwd.json") as f:
      pwd = json.load(f)
  connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                pool_size=5,
                                                pool_reset_session=True,
                                                host=host,
                                                user=user,
                                                database=database,
                                                password=password)
  connection_object = connection_pool.get_connection()
  return connection_object


select_page = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT i.url ORDER BY i.pid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid GROUP BY a.aid, a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng
ORDER BY a.aid LIMIT %s,13 
"""

select_keyword = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT i.url ORDER BY i.pid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid WHERE a.name LIKE %s OR c.category_name=%s GROUP BY a.aid, a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng
ORDER BY a.aid LIMIT %s,13 
"""

select_id = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT i.url ORDER BY i.pid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid WHERE a.id=%s GROUP BY a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng
"""

select_categories = "SELECT category_name FROM categories"

insert_user = "INSERT INTO users (name ,email, password) VALUES(%s, %s, %s)"

select_email = "SELECT email FROM users WHERE email=%s"

select_user_by_email = "SELECT uid, name, email, password FROM users WHERE email=%s"


class Users:

	def __init__(self) -> None:
		self.db = connectPool("users")


	def attractions(self, page, keyword):
		try:
			db = connectPool("users")
			mycursor = db.cursor(dictionary=True)
			start_attraction = int(page) * 12

			if keyword == "":
				mycursor.execute(select_page, (start_attraction, ))
			else:
				mycursor.execute(select_keyword, ("%" + keyword + "%", keyword, start_attraction))

			items = mycursor.fetchall()

			if len(items) == 13:
				next = True
				items.pop()
				return items, next
			else:
				next = False
				return items, next

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


	def attraction(sel, id):
		try:
			db = connectPool("users")
			mycursor = db.cursor(dictionary=True)
			mycursor.execute(select_id, (id, ))
			item = mycursor.fetchone()
			return item

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()
    

	def categories(self):
		try:
			db = connectPool("users")
			mycursor = db.cursor()
			mycursor.execute(select_categories)
			items = mycursor.fetchall()
			return items

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


	def createUser(name, email, password):
		try:
			db = connectPool("users")
			mycursor = db.cursor(buffered=True)

			mycursor.execute(select_email, (email, ))
			item = mycursor.fetchone()

			if not item:
				val = (name, email, password)
				mycursor.execute(insert_user, val)
				db.commit()
				return "created"
			else:
				return "exists"

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


	def getUser(email):
		try:
			db = connectPool("users")
			mycursor = db.cursor(dictionary=True)

			mycursor.execute(select_user_by_email, (email, ))
			item = mycursor.fetchone()

			if not item:
				return False
			else:
				return item
		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()
