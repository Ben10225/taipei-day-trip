import json
from mysql.connector import Error
from mysql.connector import pooling

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
                                                host='localhost',
                                                user='root',
                                                database='taipei',
                                                password= pwd["password"])
  connection_object = connection_pool.get_connection()
  return connection_object


select_page = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT(i.url) ORDER BY i.iid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid GROUP BY a.aid, a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, i.iid
ORDER BY a.aid LIMIT %s,13 
"""

select_keyword = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT(i.url) ORDER BY i.iid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid WHERE a.name LIKE %s OR c.category_name=%s GROUP BY a.aid, a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, i.iid
ORDER BY a.aid LIMIT %s,13 
"""

select_id = """
SELECT a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, 
GROUP_CONCAT( DISTINCT(i.url) ORDER BY i.iid ASC SEPARATOR ',') AS urls 
FROM attractions AS a
INNER JOIN categories AS c ON a.category_id=c.cid INNER JOIN mrts AS m ON a.mrt_id=m.mid 
INNER JOIN images AS i ON a.id=i.iid WHERE a.id=%s GROUP BY a.id, c.category_name, a.name, a.description, a.address, a.transport, m.mrt_name, a.lat, a.lng, i.iid
"""

select_categories = "SELECT category_name FROM categories"


# select by querystring
def db_attractions(page, keyword):
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
      return items[:-1], next
    else:
      next = False
      return items, next

  except Error as e:
    print("Error while connecting to MySQL using Connection pool ", e)

  finally:
    mycursor.close()
    db.close()


# select attraction by id
def db_attraction_by_id(id):
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


# select categories
def db_categories():
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
