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

select_all = "SELECT * FROM attractions"
select_keyword = "SELECT * FROM attractions WHERE name LIKE %s"
select_id = "SELECT * FROM attractions WHERE id=%s"
select_categories = "SELECT category FROM attractions"


# select by querystring
def db_attractions(keyword):
  try:
    db = connectPool("users")
    mycursor = db.cursor(dictionary=True)
    if keyword == "":
      mycursor.execute(select_all)
    else:
      mycursor.execute(select_keyword, ("%" + keyword + "%",))
    items = mycursor.fetchall()
    return items

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