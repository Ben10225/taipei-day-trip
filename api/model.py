from data.db_connection import *
from data.sql_command import *
from mysql.connector import Error

pool = connectPool()

class Attr:
	def attractions(page, keyword):
		try:
			db = pool.get_connection()
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
			db = pool.get_connection()
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
			db = pool.get_connection()
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
			db = pool.get_connection()
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
			db = pool.get_connection()
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
			db = pool.get_connection()
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
			db = pool.get_connection()
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

	def delete_bookings(bid, status):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True)

			if status == "multiple":
				t = tuple(i for i in bid)
				mycursor.execute(delete_booking_by_bids %f"{t}")
				db.commit()
				return True

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

	def get_user_info_by_uuid(uuid):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True, dictionary=True)

			mycursor.execute(select_name_email_by_uuid, (uuid, ))
			info = mycursor.fetchone()

			if info:
				return info["name"], info["email"]
			else:
				return False

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


class Order:
	def create_payment(number, uuid, total_price, name, email, phone, bool):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True)

			mycursor.execute(insert_payment, (number, uuid, total_price, name, email, phone, bool))
			db.commit()

			mycursor.execute(select_payment_id, )
			id = mycursor.fetchone()
			
			return id[0]

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()

	def create_trips(tid, number, a_id, a_name, a_address, a_image, a_price, a_date, a_time):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True)

			mycursor.execute(insert_trips, (tid, number, a_id, a_name, a_address, a_image, a_price, a_date, a_time))
			db.commit()

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()

	def get_order_details(payment_id, number):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True, dictionary=True)

			mycursor.execute(select_payment_by_id_and_num, (payment_id, number))
			payment = mycursor.fetchone()

			mycursor.execute(select_trips_by_id_and_num, (payment_id, number))
			trips = mycursor.fetchall()

			return payment, trips

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()


class History:
	def get_user_orders(uuid):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True, dictionary=True)

			mycursor.execute(select_payment_by_uuid_group, (uuid, ))
			orders = mycursor.fetchall()

			if len(orders) > 0:
				return orders
			else:
				return None

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()

	def update_user_name(uuid, name):
		try:
			db = pool.get_connection()
			mycursor = db.cursor(buffered=True)

			mycursor.execute(update_name, (name, uuid))
			db.commit()

		except Error as e:
			print("Error while connecting to MySQL using Connection pool ", e)
		
		finally:
			mycursor.close()
			db.close()