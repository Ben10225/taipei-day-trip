
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
"""

select_booking_by_bid = "SELECT bid FROM bookings WHERE bid=%s"

delete_booking_by_bid = "DELETE FROM bookings WHERE bid=%s"