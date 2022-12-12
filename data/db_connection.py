from mysql.connector import pooling

import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
database = os.getenv("database")
password = os.getenv("password")

def connectPool():
  connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                pool_size=5,
                                                pool_reset_session=True,
                                                host=host,
                                                user=user,
                                                database=database,
                                                password=password)
  connection_object = connection_pool.get_connection()
  return connection_object



