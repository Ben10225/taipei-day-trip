
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