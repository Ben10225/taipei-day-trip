from data.db_connection import *
from data.sql_command import *
from mysql.connector import Error


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
	def create_user(my_uuid, name, email, password):
		try:
			db = connectPool()
			mycursor = db.cursor(buffered=True)

			mycursor.execute(select_email, (email, ))
			item = mycursor.fetchone()

			if not item:
				val = (my_uuid, name, email, password)
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


	def get_user(email):
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


class Booking:
	def create_booking(uuid, attraction_Id, date, time, price, push_status):
		try:
			db = connectPool()
			mycursor = db.cursor(buffered=True)

			if push_status:
				val = (uuid, attraction_Id, date, time, price)
				mycursor.execute(insert_booking, val)
				db.commit()
				return "created_force"

			mycursor.execute(select_booking, (attraction_Id, date, time))
			item = mycursor.fetchone()

			if not item:
				val = (uuid, attraction_Id, date, time, price)
				mycursor.execute(insert_booking, val)
				db.commit()
				return "created"
			else:
				return "exists"

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()

	def get_bookings(uuid):
		try:
			db = connectPool()
			mycursor = db.cursor(buffered=True, dictionary=True)

			mycursor.execute(select_booking_by_uuid, (uuid, ))
			bookings = mycursor.fetchall()

			if bookings:
				return bookings
			else:
				return []

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()

	def delete_bookings(bid):
		try:
			db = connectPool()
			mycursor = db.cursor(buffered=True)

			mycursor.execute(select_booking_by_bid, (bid, ))
			item = mycursor.fetchone()

			if item:
				mycursor.execute(delete_booking_by_bid, (bid, ))
				db.commit()
				return True
			else:
				return False

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()