
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


# user
insert_user = "INSERT INTO users (uuid, name ,email, password) VALUES(%s, %s, %s, %s)"

select_email = "SELECT email FROM users WHERE email=%s"

select_user_by_email = "SELECT uuid, name, email, password FROM users WHERE email=%s"

# booking
select_booking = "SELECT attraction_id, date, time FROM bookings WHERE attraction_id=%s and date=%s and time=%s"

insert_booking = "INSERT INTO bookings (uuid, attraction_id, date, time, price) VALUES(%s, %s, %s, %s, %s)"

select_booking_by_uuid = """
SELECT b.bid, b.attraction_id, b.date, b.time, b.price, a.name, a.address, i.url
FROM bookings AS b
INNER JOIN attractions AS a ON b.attraction_id=a.id
INNER JOIN images AS i ON i.iid=b.attraction_id
WHERE b.uuid=%s
GROUP BY b.bid
ORDER BY b.bid ASC
"""

select_booking_by_bid = "SELECT bid FROM bookings WHERE bid=%s"

delete_booking_by_bid = "DELETE FROM bookings WHERE bid=%s"

delete_booking_by_bids = "DELETE FROM bookings WHERE bid in %s"

select_name_email_by_uuid = "SELECT name, email FROM users WHERE uuid=%s"

# order
insert_payment = "INSERT INTO payment (order_number, uuid, total_price, contact_name, contact_email, contact_phone, status) VALUES(%s, %s, %s, %s, %s, %s, %s);"

select_payment_id = "SELECT LAST_INSERT_ID(payment_id) from payment order by LAST_INSERT_ID(payment_id) DESC LIMIT 1;"

insert_trips = "INSERT INTO trips VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

select_payment_by_id_and_num = """
SELECT total_price, contact_name, contact_email, contact_phone, status 
FROM payment WHERE payment_id=%s AND order_number=%s
"""

select_trips_by_id_and_num = """
SELECT attraction_id, attraction_name, attraction_address, attraction_image, attraction_price, attraction_date, attraction_time
FROM trips WHERE tid=%s AND trip_order_number=%s
"""

# history
select_payment_by_uuid_group = """
SELECT payment_id, order_number, time FROM payment 
WHERE uuid=%s GROUP BY payment_id
ORDER BY payment_id DESC
"""

update_name = """
UPDATE users SET name=%s WHERE uuid=%s;
"""