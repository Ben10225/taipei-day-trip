from data.db_connection import *
from data.sql_command import *


def attraction_details(item):
	images = item["urls"].split(",")
	details = {
		"id": item["id"],
		"name": item["name"],
		"category": item["category_name"],
		"description": item["description"],
		"address": item["address"].replace(" ",""),
		"transport": item["transport"],
		"mrt": item["mrt_name"],
		"lat": item["lat"],
		"lng": item["lng"],
		"images": images
	}
	return details


class Attr:
	def attractions(page, keyword):
		try:
			db = connectPool()
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

	def attraction(id):
		try:
			db = connectPool()
			mycursor = db.cursor(dictionary=True)
			mycursor.execute(select_id, (id, ))
			item = mycursor.fetchone()
			return item

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()
    

	def categories():
		try:
			db = connectPool()
			mycursor = db.cursor()
			mycursor.execute(select_categories)
			items = mycursor.fetchall()
			return items

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


class User:
	def createUser(name, email, password):
		try:
			db = connectPool()
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
			db = connectPool()
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
